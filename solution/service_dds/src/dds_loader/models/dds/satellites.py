from typing import Any, Tuple

from .base import DdsModel, TableInfo
from .hubs import OrderHub, ProductHub, RestaurantHub, UserHub


class Satellite(DdsModel):
    pass
 

class UserNamesSatellite(Satellite):
    h_user: UserHub
    username: str
    userlogin: str

    @property
    def table_info(self) -> TableInfo:
        return TableInfo.s_user_names

    def get_params(self, load_src: str) -> Tuple[Tuple[str], Tuple[Any]]:
        attrs = self.model_dump(exclude='h_user')
        attrs[self.h_user.table_info.index_col] = self.h_user.get_surrogate_key()
        return super().get_params(attrs, load_src)


class ProductNamesSatellite(Satellite):
    h_product: ProductHub
    name: str

    @property
    def table_info(self) -> TableInfo:
        return TableInfo.s_product_names

    def get_params(self, load_src: str) -> Tuple[Tuple[str], Tuple[Any]]:
        attrs = self.model_dump(exclude='h_product')
        attrs[self.h_product.table_info.index_col] = self.h_product.get_surrogate_key()
        return super().get_params(attrs, load_src)


class RestaurantNamesSatellite(Satellite):
    h_restaurant: RestaurantHub
    name: str

    @property
    def table_info(self) -> TableInfo:
        return TableInfo.s_restaurant_names

    def get_params(self, load_src: str) -> Tuple[Tuple[str], Tuple[Any]]:
        attrs = self.model_dump(exclude='h_restaurant')
        attrs[self.h_restaurant.table_info.index_col] = self.h_restaurant.get_surrogate_key()
        return super().get_params(attrs, load_src)


class OrderCostSatellite(Satellite):
    h_order: OrderHub
    cost: int
    payment: int

    @property
    def table_info(self) -> TableInfo:
        return TableInfo.s_order_cost

    def get_params(self, load_src: str) -> Tuple[Tuple[str], Tuple[Any]]:
        attrs = self.model_dump(exclude='h_order')
        attrs[self.h_order.table_info.index_col] = self.h_order.get_surrogate_key()
        return super().get_params(attrs, load_src)


class OrderStatusSatellite(Satellite):
    h_order: OrderHub
    status: str

    @property
    def table_info(self) -> TableInfo:
        return TableInfo.s_order_status

    def get_params(self, load_src: str) -> Tuple[Tuple[str], Tuple[Any]]:
        attrs = self.model_dump(exclude='h_order')
        attrs[self.h_order.table_info.index_col] = self.h_order.get_surrogate_key()
        return super().get_params(attrs, load_src)
