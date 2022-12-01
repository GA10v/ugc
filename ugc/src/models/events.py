from datetime import datetime
from random import choice, randint
from typing import Union
from uuid import UUID, uuid4

from core.config import settings
from pydantic import BaseModel


class RatingEvent(BaseModel):
    user_id: str
    movie_id: str
    evetn: int
    event_time: datetime

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['event_time'] = _dict['event_time'].strftime('%Y-%m-%d %H:%M:%S')
        return _dict


class ViewsEvent(BaseModel):
    user_id: UUID
    movie_id: UUID
    evetn: int
    event_time: datetime

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['event_time'] = _dict['event_time'].strftime('%Y-%m-%d %H:%M:%S')
        return _dict


events = Union[RatingEvent, ViewsEvent]


class Event(BaseModel):
    event_type: str
    event: events
    # event_time: datetime

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        # _dict['event_time'] = _dict['event_time'].strftime('%Y-%m-%d %H:%M:%S')
        return _dict


def fake_batch(batch_size: int) -> list[Event]:
    def _fake_event(event_type: str) -> events:
        if event_type == 'rating':
            return RatingEvent(
                movie_id=str(uuid4()), user_id=str(uuid4()), evetn=randint(1, 10), event_time=datetime.now()
            )
        if event_type == 'views':
            return ViewsEvent(
                movie_id=str(uuid4()), user_id=str(uuid4()), evetn=randint(1, 180), event_time=datetime.now()
            )

    fake_batch = []
    for _ in range(batch_size):
        _event_type = choice(settings.kafka.TOPICS)
        _event: Event = (Event(event_type=_event_type, event_time=datetime.now(), event=_fake_event(_event_type)),)
        fake_batch.append(_event)
    return fake_batch
