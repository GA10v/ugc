from datetime import datetime
from typing import Union
from uuid import UUID

from pydantic import BaseModel


class RatingEvent(BaseModel):
    user_id: str
    movie_id: str
    evetn: int
    event_time: datetime


class ViewsEvent(BaseModel):
    user_id: UUID
    movie_id: UUID
    evetn: int
    event_time: datetime


events = Union[RatingEvent, ViewsEvent]


class Event(BaseModel):
    event_type: str
    event: events
    event_time: datetime
