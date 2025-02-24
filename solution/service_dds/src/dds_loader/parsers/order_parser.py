import json
from datetime import datetime
from functools import cached_property
from typing import List, Tuple, Set

from pydantic import BaseModel, Field, computed_field

from dds_loader.models import dds, stg
from dds_loader.models.dds import Hub, Link, Satellite


class UserSerializer(BaseModel):
    user_id: str = Field(alias='id')
    username: str = Field(alias='name')
    userlogin: str = Field(alias='login')

    @computed_field
    @cached_property
    def h_user(self) -> dds.UserHub:
        return dds.UserHub(**self.__dict__)

    @computed_field
    @cached_property
    def s_user_names(self) -> dds.UserNamesSatellite:
        return dds.UserNamesSatellite(**self.__dict__)


class RestaurantSerializer(BaseModel):
    restaurant_id: str = Field(alias='id')
    name: str

    @computed_field
    @cached_property
    def h_restaurant(self) -> dds.RestaurantHub:
        return dds.RestaurantHub(**self.__dict__)

    @computed_field
    @cached_property
    def s_restaurant_names(self) -> dds.RestaurantNamesSatellite:
        return dds.RestaurantNamesSatellite(**self.__dict__)


class OrderSerializer(BaseModel):
    order_id: int = Field(alias='id')
    order_dt: datetime = Field(alias='date')
    cost: int
    payment: int
    status: str
    user: UserSerializer

    @computed_field
    @cached_property
    def h_order(self) -> dds.OrderHub:
        return dds.OrderHub(**self.__dict__)

    @computed_field
    @cached_property
    def s_order_status(self) -> dds.OrderStatusSatellite:
        return dds.OrderStatusSatellite(**self.__dict__)

    @computed_field
    @cached_property
    def s_order_cost(self) -> dds.OrderCostSatellite:
        return dds.OrderCostSatellite(**self.__dict__)

    @computed_field
    @cached_property
    def l_order_user(self) -> dds.OrderUserLink:
        return dds.OrderUserLink(h_user=self.user.h_user, **self.__dict__)


class ProductSerializer(BaseModel):
    product_id: str = Field(alias='id')
    name: str
    category_name: str = Field(alias='category')
    order: OrderSerializer
    restaurant: RestaurantSerializer

    @computed_field
    @cached_property
    def h_product(self) -> dds.ProductHub:
        return dds.ProductHub(**self.__dict__)

    @computed_field
    @cached_property
    def h_category(self) -> dds.CategoryHub:
        return dds.CategoryHub(**self.__dict__)

    @computed_field
    @cached_property
    def s_product_names(self) -> dds.ProductNamesSatellite:
        return dds.ProductNamesSatellite(**self.__dict__)

    @computed_field
    @cached_property
    def l_product_category(self) -> dds.ProductCategoryLink:
        return dds.ProductCategoryLink(**self.__dict__)

    @computed_field
    @cached_property
    def l_order_product(self) -> dds.OrderProductLink:
        return dds.OrderProductLink(h_order=self.order.h_order, **self.__dict__)

    @computed_field
    @cached_property
    def l_product_restaurant(self) -> dds.ProductRestaurantLink:
        return dds.ProductRestaurantLink(h_restaurant=self.restaurant.h_restaurant, **self.__dict__)


class OrderParser(BaseModel):
    user: UserSerializer
    restaurant: RestaurantSerializer
    order: OrderSerializer
    products: List[ProductSerializer]

    @classmethod
    def from_valid(cls, data: stg.Order) -> 'OrderParser':
        user = UserSerializer(**data.pop('user'))
        restaurant = RestaurantSerializer(**data.pop('restaurant'))
        order = OrderSerializer(user=user, **data)
        products = [
            ProductSerializer(order=order, restaurant=restaurant, **p) for p in data['products']
        ]
        return OrderParser(user=user, restaurant=restaurant, order=order, products=products)


    def get_data_vault(self) -> Tuple[Set[Hub], Set[Link], Set[Satellite]]:
        hubs, links, satellites = set(), set(), set()

        for obj in (self.user, self.restaurant, self.order, *self.products):
            for attr, info in obj.model_computed_fields.items():
                item = getattr(obj, attr)

                if issubclass(info.return_type, Hub):
                    hubs.add(item)
                elif issubclass(info.return_type, Link):
                    links.add(item)
                elif issubclass(info.return_type, Satellite):
                    satellites.add(item)

        return hubs, links, satellites


    def get_output(self) -> str:
        data = {}
        data['object_id'] = str(self.user.h_user.get_surrogate_key())
        data['object_type'] = 'user_products'
        data['payload'] = {
            'id': data['object_id'],
            'products': [
                {
                    'id': str(p.h_product.get_surrogate_key()),
                    'name': p.name,
                    'category': {
                        'id': str(p.h_category.get_surrogate_key()),
                        'name': p.category_name
                    }
                } for p in self.products
            ]
        }
        return json.dumps(data)
