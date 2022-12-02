from typing import Union

from pydantic import BaseModel


class RatingEvent(BaseModel):
    user_id: str
    movie_id: str
    evetn: int
    event_time: str


class ViewsEvent(BaseModel):
    user_id: str
    movie_id: str
    evetn: int
    event_time: str


events = Union[RatingEvent, ViewsEvent]


class EventKafka(BaseModel):
    event_type: str
    event: events
