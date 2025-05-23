import os

from lib.kafka_connect import KafkaConsumer
from lib.pg import PgConnect


class AppConfig:
    CERTIFICATE_PATH = '/crt/YandexInternalRootCA.crt'
    DEFAULT_JOB_INTERVAL = 25

    def __init__(self) -> None:
        # KAFKA CONSUMER
        self.kafka_host = str(os.getenv('KAFKA_HOST', ''))
        self.kafka_port = int(str(os.getenv('KAFKA_PORT', 0)))
        self.kafka_consumer_username = str(os.getenv('KAFKA_CONSUMER_USERNAME', ''))
        self.kafka_consumer_password = str(os.getenv('KAFKA_CONSUMER_PASSWORD', ''))
        self.kafka_consumer_group = str(os.getenv('KAFKA_CONSUMER_GROUP', ''))
        self.kafka_consumer_topic = str(os.getenv('KAFKA_SOURCE_TOPIC', ''))
        # POSTGRES WAREHOUSE
        self.pg_warehouse_host = str(os.getenv('PG_WAREHOUSE_HOST', ''))
        self.pg_warehouse_port = int(str(os.getenv('PG_WAREHOUSE_PORT', 0)))
        self.pg_warehouse_dbname = str(os.getenv('PG_WAREHOUSE_DBNAME', ''))
        self.pg_warehouse_user = str(os.getenv('PG_WAREHOUSE_USER', ''))
        self.pg_warehouse_password = str(os.getenv('PG_WAREHOUSE_PASSWORD', ''))


    def kafka_consumer(self):
        return KafkaConsumer(
            self.kafka_host,
            self.kafka_port,
            self.kafka_consumer_username,
            self.kafka_consumer_password,
            self.kafka_consumer_topic,
            self.kafka_consumer_group,
            self.CERTIFICATE_PATH
        )

    def pg_warehouse_db(self):
        return PgConnect(
            self.pg_warehouse_host,
            self.pg_warehouse_port,
            self.pg_warehouse_dbname,
            self.pg_warehouse_user,
            self.pg_warehouse_password
        )
