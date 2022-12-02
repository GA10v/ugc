import asyncio
import json
from collections import defaultdict
from functools import lru_cache
from datetime import datetime
from uuid import UUID
from typing import Optional, Tuple

from aiokafka import AIOKafkaProducer
from core.config import settings
from fastapi import Request, Response, Depends
from models.events import Event, EventInfo, fake_batch
from services.broker.protocol import ProducerProtocol


# loop = asyncio.get_event_loop()
# aioproducer = AIOKafkaProducer(loop=loop, **settings.kafka.producer_conf)
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

    def _get_user_id(self) -> str | UUID:
        return '1f9e1fc2-443f-46e9-bccf-0b406a1082b4'

    @staticmethod
    def _get_event(user_id: str | UUID, movie_id: str | UUID, event: int, event_type: str) -> Event:
        return Event(
            event_type=event_type,
            event_info=EventInfo(
                user_id=user_id,
                movie_id=movie_id,
                event=event,
                event_time=datetime.now()
            )
        )

    @staticmethod
    def _parse_event(event: Event) -> Tuple[str | UUID, str | UUID, str]:
        return event.event_info.user_id, event.event_info.movie_id, event.event_type

    async def produce(self, movie_id: str | UUID, event: int, event_type: str) -> Event:
        user_id = self._get_user_id()
        event = self._get_event(user_id, movie_id, event, event_type)
        await self.aioproducer.send_and_wait(
            topic=event_type,
            value=self._serialize(event),
            key=self._create_key(user_id, movie_id, event_type)
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
                timestamp=None
            )
        print(batch_dict['rating'].record_count(), batch_dict['views'].record_count())
        for topic in batch_dict:
            batch = batch_dict[topic]
            batch.close()
            fut = await self.aioproducer.send_batch(batch, topic=topic, partition=0)
            print(await fut)


# producer: KafkaProducer = KafkaProducer()


@lru_cache()
def get_producer(aioproducer: AIOKafkaProducer = Depends(get_aioproducer)) -> KafkaProducer:
    return KafkaProducer(aioproducer)
