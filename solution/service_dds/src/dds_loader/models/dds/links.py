from typing import Any, Tuple

from .base import DdsModel, TableInfo
from .hubs import OrderHub, ProductHub, CategoryHub, RestaurantHub, UserHub


class Link(DdsModel):
    pass


class OrderProductLink(Link):
    h_order: OrderHub
    h_product: ProductHub

    @property
    def table_info(self) -> TableInfo:
        return TableInfo.l_order_product

    def get_params(self, load_src: str) -> Tuple[Tuple[str], Tuple[Any]]:
        attrs = {}
        attrs[self.h_order.table_info.index_col] = self.h_order.get_surrogate_key()
        attrs[self.h_product.table_info.index_col] = self.h_product.get_surrogate_key()
        return super().get_params(attrs, load_src)


class ProductRestaurantLink(Link):
    h_product: ProductHub
    h_restaurant: RestaurantHub

    @property
    def table_info(self) -> TableInfo:
        return TableInfo.l_product_restaurant

    def get_params(self, load_src: str) -> Tuple[Tuple[str], Tuple[Any]]:
        attrs = {}
        attrs[self.h_product.table_info.index_col] = self.h_product.get_surrogate_key()
        attrs[self.h_restaurant.table_info.index_col] = self.h_restaurant.get_surrogate_key()
        return super().get_params(attrs, load_src)


class ProductCategoryLink(Link):
    h_product: ProductHub
    h_category: CategoryHub

    @property
    def table_info(self) -> TableInfo:
        return TableInfo.l_product_category

    def get_params(self, load_src: str) -> Tuple[Tuple[str], Tuple[Any]]:
        attrs = {}
        attrs[self.h_product.table_info.index_col] = self.h_product.get_surrogate_key()
        attrs[self.h_category.table_info.index_col] = self.h_category.get_surrogate_key()
        return super().get_params(attrs, load_src)


class OrderUserLink(Link):
    h_order: OrderHub
    h_user: UserHub

    @property
    def table_info(self) -> TableInfo:
        return TableInfo.l_order_user

    def get_params(self, load_src: str) -> Tuple[Tuple[str], Tuple[Any]]:
        attrs = {}
        attrs[self.h_order.table_info.index_col] = self.h_order.get_surrogate_key()
        attrs[self.h_user.table_info.index_col] = self.h_user.get_surrogate_key()
        return super().get_params(attrs, load_src)
