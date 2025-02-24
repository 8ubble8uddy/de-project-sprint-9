from typing import Set, Union

from lib.pg import PgConnect
from cdm_loader.models.cdm import UserCategory, UserProduct
 

class CdmRepository:
    def __init__(self, db: PgConnect) -> None:
        self._db = db

    def user_counters_insert(self, user_agg: Set[Union[UserCategory, UserProduct]]) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:

                for item in user_agg:
                    keys, values = item.get_params()
                    table_name, constraint_name = item.table_info

                    query = f"""
                        INSERT INTO cdm.{table_name} ({', '.join(keys)})
                        VALUES ({', '.join(f"'{v}'" for v in values)})
                        ON CONFLICT ON CONSTRAINT {constraint_name}
                        DO UPDATE SET order_cnt = cdm.{table_name}.order_cnt + 1;
                    """
                    cur.execute(query)
