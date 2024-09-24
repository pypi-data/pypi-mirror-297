from typing import Any
from uuid import UUID

from aiokafka import AIOKafkaProducer
from pydantic import BaseModel

from .event_types_enum import EventTypeEnum


class KafkaProducer:
    def __init__(self, client: AIOKafkaProducer):
        self._client = client

    async def send_and_wait(
            self,
            topic: str,
            value: BaseModel | UUID,
            event_type: EventTypeEnum,
    ) -> Any:
        return await self._client.send_and_wait(
            topic=topic,
            value=value,
            key=event_type,
        )
