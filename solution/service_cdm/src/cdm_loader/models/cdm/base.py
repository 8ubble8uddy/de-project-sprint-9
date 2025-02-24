from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Tuple

from pydantic import BaseModel


class TableInfo(Enum):  #       TABLE NAME                  UNIQUE CONSTRAINT NAME
    user_category_counters =    'user_category_counters',   'user_id_category_id_uindex'
    user_product_counters =     'user_product_counters',    'user_id_product_id_uindex'

    def __init__(self, table_name, constraint_name):
        self.table_name = table_name
        self.constraint_name = constraint_name

    def __getitem__(self, index):
        return self.value[index]


class CdmModel(ABC, BaseModel, frozen=True):

    @property
    @abstractmethod
    def table_info(self) -> TableInfo:
        ...

    def get_params(self) -> Tuple[Tuple[str], Tuple[Any]]:
        attrs = self.model_dump()
        attrs['order_cnt'] = 1
        keys, values = zip(*attrs.items())
        return keys, values
