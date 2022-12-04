from datetime import datetime
from typing import Union

from pydantic import BaseModel


class RatingEvent(BaseModel):
    user_id: str
    movie_id: str
    event: int
    event_time: datetime


class ViewsEvent(BaseModel):
    user_id: str
    movie_id: str
    event: int
    event_time: datetime


events = Union[RatingEvent, ViewsEvent]


class EventKafka(BaseModel):
    event_type: str
    event_payload: events


event_models = {
    'rating': RatingEvent,
    'views': ViewsEvent,
}
