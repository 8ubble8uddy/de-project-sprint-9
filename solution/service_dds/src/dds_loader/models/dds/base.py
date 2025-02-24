from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from functools import lru_cache
from typing import Any, Dict, Tuple
from uuid import UUID

from pydantic import BaseModel

from lib.utils import formatting_dt, create_uuid_from_string


class TableInfo(Enum):  #   TABLENAME               INDEX COLUMN                CONFLICT ACTION
    h_user =                'h_user',               'h_user_pk',                    'NOTHING'
    h_product =             'h_product',            'h_product_pk',                 'NOTHING'
    h_category =            'h_category',           'h_category_pk',                'NOTHING'
    h_restaurant =          'h_restaurant',         'h_restaurant_pk',              'NOTHING'
    h_order =               'h_order',              'h_order_pk',                   'NOTHING'
    l_order_product =       'l_order_product',      'hk_order_product_pk',          'NOTHING'
    l_product_restaurant =  'l_product_restaurant', 'hk_product_restaurant_pk',     'NOTHING'
    l_product_category =    'l_product_category',   'hk_product_category_pk',       'NOTHING'
    l_order_user =          'l_order_user',         'hk_order_user_pk',             'NOTHING'
    s_user_names =          's_user_names',         'hk_user_names_hashdiff',       'UPDATE'
    s_product_names =       's_product_names',      'hk_product_names_hashdiff',    'UPDATE'
    s_restaurant_names =    's_restaurant_names',   'hk_restaurant_names_hashdiff', 'UPDATE'
    s_order_cost =          's_order_cost',         'hk_order_cost_hashdiff',       'UPDATE'
    s_order_status =        's_order_status',       'hk_order_status_hashdiff',     'UPDATE'

    def __init__(self, table_name, index_col, conflict_action):
        self.table_name = table_name
        self.index_col = index_col
        self.conflict_action = conflict_action

    def __getitem__(self, index):
        return self.value[index]


class DdsModel(ABC, BaseModel, frozen=True):

    def __str__(self) -> str:
        attrs_str = ''.join(map(str, self.__dict__.values()))
        return attrs_str

    @lru_cache
    def get_surrogate_key(self) -> UUID:
        return create_uuid_from_string(str(self))

    @property
    @abstractmethod
    def table_info(self) -> TableInfo:
        ...

    def get_params(self, attrs: Dict, load_src: str) -> Tuple[Tuple[str], Tuple[Any]]:
        attrs['load_src'] = load_src
        attrs['load_dt'] = formatting_dt(datetime.utcnow())
        attrs[self.table_info.index_col] = self.get_surrogate_key()
        keys, values = zip(*attrs.items())
        return keys, values
