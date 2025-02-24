from typing import Set

from lib.pg import PgConnect
from dds_loader.models.dds import Hub, Link, Satellite
 

class DdsRepository:
    def __init__(self, db: PgConnect) -> None:
        self._db = db

    def load_dds(self, hubs: Set[Hub], links: Set[Link], satellites: Set[Satellite], load_src: str = 'stg-service-kafka') -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:

                for item in (*hubs, *links, *satellites):
                    keys, values = item.get_params(load_src)
                    table_name, index_col, conflict_action = item.table_info

                    if conflict_action == 'UPDATE':
                        conflict_action = '{action} SET {expressions}'.format(
                            action=conflict_action,
                            expressions=', '.join([f'{col} = EXCLUDED.{col}' for col in keys]))
                    
                    query = f"""
                        INSERT INTO dds.{table_name} ({', '.join(keys)})
                        VALUES ({', '.join(f"'{v}'" for v in values)})
                        ON CONFLICT ({index_col})
                        DO {conflict_action};
                    """
                    cur.execute(query)
