import orjson
from datetime import datetime
from random import choice, randint
from typing import Union, Optional
from uuid import UUID, uuid4

from core.config import settings
from pydantic import BaseModel
from .base import BaseOrjsonModel


class EventInfo(BaseOrjsonModel):
    user_id: str | UUID
    movie_id: str | UUID
    event: int
    event_time: datetime

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        _dict['event_time'] = _dict['event_time'].strftime('%Y-%m-%d %H:%M:%S')
        return _dict


# class ViewsEvent(BaseModel):
#     user_id: UUID
#     movie_id: UUID
#     evetn: int
#     event_time: datetime
#
#     def dict(self, *args, **kwargs) -> dict:
#         _dict: dict = super().dict(*args, **kwargs)
#         _dict['event_time'] = _dict['event_time'].strftime('%Y-%m-%d %H:%M:%S')
#         return _dict


# events = Union[RatingEvent, ViewsEvent]

class Event(BaseOrjsonModel):
    event_type: str
    event_info: EventInfo
    # event_time: datetime

    def dict(self, *args, **kwargs) -> dict:
        _dict: dict = super().dict(*args, **kwargs)
        # _dict['event_time'] = _dict['event_time'].strftime('%Y-%m-%d %H:%M:%S')
        return _dict


def fake_batch(batch_size: int) -> list[Event]:
    def _fake_event(event_type: str) -> Optional[EventInfo]:
        if event_type == 'rating':
            event = randint(1, 100)
        elif event_type == 'views':
            event = randint(1, 10000)
        else:
            return

        return EventInfo(
            movie_id=str(uuid4()), user_id=str(uuid4()), event=event, event_time=datetime.now()
        )

    fake_batch = []
    for _ in range(batch_size):
        _event_type = choice(settings.kafka.TOPICS)
        _event: Event = Event(event_type=_event_type, event_info=_fake_event(_event_type))
        if _event:
            fake_batch.append(_event)
    return fake_batch