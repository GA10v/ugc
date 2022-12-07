from datetime import datetime
from typing import Union
from uuid import UUID

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseOrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class RatingEvent(BaseOrjsonModel):
    user_id: str
    movie_id: str
    evetn: int
    event_time: datetime


class ViewsEvent(BaseOrjsonModel):
    user_id: UUID
    movie_id: UUID
    evetn: int
    event_time: datetime


events = Union[RatingEvent, ViewsEvent]


class Event(BaseOrjsonModel):
    event_type: str
    event: events
    event_time: datetime
