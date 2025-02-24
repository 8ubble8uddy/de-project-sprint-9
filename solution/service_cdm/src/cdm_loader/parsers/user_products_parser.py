from typing import List, Set
from uuid import UUID

from pydantic import BaseModel, Field, computed_field

from cdm_loader.models import dds, cdm
from cdm_loader.models.cdm.user_agg import UserAgg


class CategorySerializer(BaseModel):
    category_id: UUID = Field(alias='id')
    category_name: str = Field(alias='name')


class ProductSerializer(BaseModel):
    product_id: UUID = Field(alias='id')
    product_name: str = Field(alias='name')
    category: CategorySerializer


class UserProductSerializer(BaseModel):
    id: UUID
    product: ProductSerializer

    @computed_field
    def user_product(self) -> cdm.UserProduct:
        return cdm.UserProduct(user_id=self.id, **self.product.__dict__)
    
    @computed_field
    def user_category(self) -> cdm.UserCategory:
        return cdm.UserCategory(user_id=self.id, **self.product.category.__dict__)


class UserProductsParser(BaseModel):
    user_products: List[UserProductSerializer]

    @classmethod
    def from_valid(cls, data: dds.UserProducts) -> 'UserProductsParser':
        user_products = [
            UserProductSerializer(id=data['id'], product=p) for p in data['products']
        ]
        return UserProductsParser(user_products=user_products)


    def get_user_agg(self) -> Set[UserAgg]:
        user_agg = set()
        for obj in self.user_products:
            for attr, info in obj.model_computed_fields.items():
                item = getattr(obj, attr)

                if issubclass(info.return_type, UserAgg):
                    user_agg.add(item)

        return user_agg
