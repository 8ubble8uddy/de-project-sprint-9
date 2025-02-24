from datetime import datetime
from typing import Any, Tuple

from lib.utils import formatting_dt
from .base import DdsModel, TableInfo


class Hub(DdsModel):

    def get_params(self, load_src: str) -> Tuple[Tuple[str], Tuple[Any]]:
        attrs = self.model_dump()
        return super().get_params(attrs, load_src)


class UserHub(Hub):
    user_id: str

    @property
    def table_info(self) -> TableInfo:
        return TableInfo.h_user


class ProductHub(Hub):
    product_id: str

    @property
    def table_info(self) -> TableInfo:
        return TableInfo.h_product


class CategoryHub(Hub):
    category_name: str

    @property
    def table_info(self) -> TableInfo:
        return TableInfo.h_category


class RestaurantHub(Hub):
    restaurant_id: str

    @property
    def table_info(self) -> TableInfo:
        return TableInfo.h_restaurant


class OrderHub(Hub):
    order_id: int
    order_dt: datetime

    @property
    def table_info(self) -> TableInfo:
        return TableInfo.h_order

    def get_params(self, load_src: str) -> Tuple[Tuple[str], Tuple[Any]]:
        attrs = self.model_dump()
        attrs['order_dt'] = formatting_dt(self.order_dt)
        return DdsModel.get_params(self, attrs, load_src)
