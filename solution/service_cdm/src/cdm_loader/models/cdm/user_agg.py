from uuid import UUID

from .base import CdmModel, TableInfo


class UserAgg(CdmModel):
    user_id: UUID


class UserProduct(UserAgg):
    product_id: UUID
    product_name: str

    @property
    def table_info(self) -> TableInfo:
        return TableInfo.user_product_counters


class UserCategory(UserAgg):
    category_id: UUID
    category_name: str

    @property
    def table_info(self) -> TableInfo:
        return TableInfo.user_category_counters
