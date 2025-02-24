from typing import Literal, List
from typing_extensions import TypedDict
from uuid import UUID

from pydantic import BaseModel


class Category(TypedDict):
    id: UUID
    name: str


class Product(TypedDict):
    id: UUID
    name: str
    category: Category


class UserProducts(TypedDict):
    id: UUID
    products: List[Product]


class UserProductsMessage(BaseModel):
    object_id: UUID
    object_type: Literal['user_products']
    payload: UserProducts
