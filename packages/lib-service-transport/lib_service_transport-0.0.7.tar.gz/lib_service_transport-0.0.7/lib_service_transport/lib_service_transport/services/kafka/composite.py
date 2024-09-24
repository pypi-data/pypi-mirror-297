from aiokafka import ConsumerRecord
from pydantic import BaseModel

from .base_consumer import BaseConsumerKafka


class KafkaComposite:
    consumers: dict[str, BaseConsumerKafka] = {}

    async def add_consumer(
            self,
            event_type: str,
            consumer: BaseConsumerKafka,
    ) -> None:
        self.consumers[event_type] = consumer

    async def get_handler(self, event_type: str) -> BaseConsumerKafka:
        try:
            return self.consumers[event_type]
        except KeyError:
            pass

    async def run(self, record: ConsumerRecord) -> None:
        event_type = await self.get_event_type(record=record)
        handler = await self.get_handler(event_type=event_type)
        incoming_message = await self.get_incoming_message(
            record=record,
            incoming_message_schema=handler.incoming_message_schema,
        )

        await handler.on_request(incoming_message=incoming_message)

    @classmethod
    async def get_event_type(cls, record: ConsumerRecord) -> str:
        return record.key.decode()

    @classmethod
    async def get_incoming_message(
            cls,
            record: ConsumerRecord,
            incoming_message_schema: BaseModel,
    ) -> BaseModel:
        try:
            return incoming_message_schema.model_validate_json(record.value)
        except Exception:
            pass
