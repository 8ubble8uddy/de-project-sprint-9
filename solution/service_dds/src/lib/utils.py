import hashlib
from datetime import datetime
from uuid import UUID


def create_uuid_from_string(val: str) -> UUID:
    hex_string = hashlib.md5(val.encode('UTF-8')).hexdigest()
    return UUID(hex=hex_string)


def formatting_dt(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%d %H:%M:%S')
