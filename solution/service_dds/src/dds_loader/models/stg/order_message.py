from datetime import datetime
from typing import List, Literal
from typing_extensions import TypedDict

from pydantic import BaseModel


class User(TypedDict):
    id: str
    name: str
    login: str
    

class Restaurant(TypedDict):
    id: str
    name: str


class Product(TypedDict):
    id: str
    price: int
    quantity: int
    name: str
    category: str


class Order(TypedDict):
    id: int
    date: datetime
    cost: int
    payment: int
    status: str
    restaurant: Restaurant
    user: User
    products: List[Product]


class OrderMessage(BaseModel):
    object_id: int
    object_type: Literal['order']
    payload: Order
