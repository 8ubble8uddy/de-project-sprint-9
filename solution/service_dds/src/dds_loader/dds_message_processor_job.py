from datetime import datetime
from logging import Logger
from typing import Dict, Union

from pydantic import RootModel, Field, ValidationError

from lib.kafka_connect import KafkaConsumer, KafkaProducer
from lib.pg import PgConnect
from dds_loader.models.stg import OrderMessage
from dds_loader.parsers import OrderParser
from dds_loader.repository import DdsRepository


class Message(RootModel):
    root: Union[OrderMessage, ] = Field(discriminator='object_type')


class DdsMessageProcessor:
    def __init__(self,
                 consumer: KafkaConsumer,
                 producer: KafkaProducer,
                 postgres_db: PgConnect,
                 batch_size: int,
                 logger: Logger
                 ) -> None:
        self._consumer = consumer
        self._producer = producer
        self._dds_repository = DdsRepository(postgres_db)
        self._batch_size = batch_size
        self._logger = logger

 
    def run(self) -> None:
        self._logger.error(f'{datetime.utcnow()}: START')

        for _ in range(self._batch_size):
            data = self._consumer.consume()
            if not data:
                break
        
            msg = self.get_message(data)
            if isinstance(msg, OrderMessage):
                self._logger.info(f'Loading order numbered {msg.object_id}')
                output = self.load_order(msg.payload)
            else:
                continue

            self._producer.produce(output)

        self._logger.info(f'{datetime.utcnow()}: FINISH')


    def get_message(self, data: bytes) -> Union[OrderMessage, None]:
        try:
            obj = Message.model_validate_json(data)
        except ValidationError as exc:
            self._logger.error(exc)
            return None
        return obj.root


    def load_order(self, order: Dict) -> str:
        parser = OrderParser.from_valid(order)
        hubs, links, satellites = parser.get_data_vault()
        
        self._dds_repository.load_dds(hubs, links, satellites)
        self._logger.info('Order loaded!')

        output = parser.get_output()
        return output
