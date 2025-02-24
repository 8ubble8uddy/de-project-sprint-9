from datetime import datetime
from logging import Logger
from typing import Dict, Union

from pydantic import RootModel, Field, ValidationError
from cdm_loader.models.dds import UserProductsMessage
from cdm_loader.parsers import UserProductsParser
from cdm_loader.repository import CdmRepository

from lib.kafka_connect import KafkaConsumer
from lib.pg import PgConnect


class Message(RootModel):
    root: Union[UserProductsMessage, ] = Field(discriminator='object_type')


class CdmMessageProcessor:
    def __init__(self,
                 consumer: KafkaConsumer,
                 postgres_db: PgConnect,
                 batch_size: int,
                 logger: Logger
                 ) -> None:
        self._consumer = consumer
        self._cdm_repository = CdmRepository(postgres_db)
        self._batch_size = 100
        self._logger = logger

    def run(self) -> None:
        self._logger.info(f"{datetime.utcnow()}: START")

        for _ in range(self._batch_size):
            data = self._consumer.consume()
            if not data:
                break
        
            msg = self.get_message(data)
            if isinstance(msg, UserProductsMessage):
                self._logger.info(f'Loading products by user numbered {msg.object_id}')
                self.load_user_products(msg.payload)

        self._logger.info(f"{datetime.utcnow()}: FINISH")
    

    def get_message(self, data: bytes) -> Union[UserProductsMessage, None]:
        try:
            obj = Message.model_validate_json(data)
        except ValidationError as exc:
            self._logger.error(exc)
            return None
        return obj.root


    def load_user_products(self, user_products: Dict) -> None:
        parser = UserProductsParser.from_valid(user_products)
        user_agg = parser.get_user_agg()

        self._cdm_repository.user_counters_insert(user_agg)
        self._logger.info(f'User products loaded!')
