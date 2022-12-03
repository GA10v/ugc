import json
from collections import defaultdict
from datetime import datetime
from functools import lru_cache
from typing import Optional, Tuple
from uuid import UUID

from aiokafka import AIOKafkaProducer
from fastapi import Depends

from models.events import Event, EventInfo, EventRating, fake_batch
from services.broker.protocol import ProducerProtocol

aioproducer: Optional[AIOKafkaProducer] = None


async def get_aioproducer() -> AIOKafkaProducer:
    return aioproducer


class KafkaProducer(ProducerProtocol):
    def __init__(self, aioproducer: AIOKafkaProducer) -> None:
        self.aioproducer = aioproducer

    @staticmethod
    def _serialize(event: Event) -> bytes:
        return json.dumps(event.dict()).encode('utf-8')

    @staticmethod
    def _create_key(user_id: str | UUID, movie_id: str | UUID, event_type: str) -> Optional[bytes]:
        if event_type == 'views':
            return ':'.join([user_id, movie_id]).encode('utf-8')
        elif event_type == 'rating':
            return movie_id.encode('utf-8')

    def _get_user_id(self) -> str:
        return '1f9e1fc2-443f-46e9-bccf-0b406a1082b4'

    @staticmethod
    def _get_event(user_id: str | UUID, movie_id: str | UUID, event: int, event_type: str) -> Optional[Event]:
        if event_type == 'views':
            return Event(
                event_type=event_type,
                event_payload=EventInfo(user_id=user_id, movie_id=movie_id, event=event, event_time=datetime.now()),
            )
        if event_type == 'rating':
            return Event(
                event_type=event_type,
                event_payload=EventRating(user_id=user_id, movie_id=movie_id, event=event, event_time=datetime.now()),
            ).dict()

    @staticmethod
    def _parse_event(event: Event) -> Tuple[str | UUID, str | UUID, str]:
        return event.event_info.user_id, event.event_info.movie_id, event.event_type

    async def produce(self, movie_id: str | UUID, event: int, event_type: str, user_id: str | UUID) -> Event:
        # user_id = self._get_user_id()
        event = self._get_event(user_id, movie_id, event, event_type)
        await self.aioproducer.send_and_wait(
            topic=event_type,
            value=self._serialize(event),
            key=self._create_key(user_id, movie_id, event_type),
        )
        return event

    async def batch_produce(self, batch_size: int):
        event_list = fake_batch(batch_size)
        batch_dict = defaultdict(self.aioproducer.create_batch)
        for event in event_list:
            user_id, movie_id, event_type = self._parse_event(event)
            batch_dict[event_type].append(
                value=self._serialize(event),
                key=self._create_key(user_id, movie_id, event_type),
                timestamp=None,
            )

        for topic in batch_dict:
            batch = batch_dict[topic]
            batch.close()
            fut = await self.aioproducer.send_batch(batch, topic=topic, partition=0)
            await fut


@lru_cache()
def get_producer(aioproducer: AIOKafkaProducer = Depends(get_aioproducer)) -> KafkaProducer:
    return KafkaProducer(aioproducer)
