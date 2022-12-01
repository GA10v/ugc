import json
from uuid import UUID

from aiokafka import AIOKafkaProducer
from core.config import settings
from fastapi import Request, Response
from models.events import Event
from services.broker.protocol import ProducerProtocol

aioproducer = AIOKafkaProducer(**settings.kafka.producer_conf)


class KafkaProducer(ProducerProtocol):
    def __init__(self, aioproducer: AIOKafkaProducer = aioproducer) -> None:
        self.aioproducer = aioproducer

    @staticmethod
    def _serialize(value):
        return json.dumps(value).encode('utf-8')

    def _get_user_id(self):
        ...

    def _get_event(self, user_id, muvie_id, event_type):
        ...

    async def produce(self, movie_id: str | UUID, event: int, event_type: str):
        self._get_user_id
        self._get_event

    async def batch_produce(self):
        ...


producer: KafkaProducer = KafkaProducer()


async def get_producer() -> producer:
    return producer
