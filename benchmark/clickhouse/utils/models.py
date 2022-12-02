from typing import TypedDict
from datetime import datetime


class Event(TypedDict):
    """
    TypedDict

    user_id: str
    movie_id: str
    evetn: int
    event_time: datetime

    """

    user_id: str
    movie_id: str
    evetn: int
    event_time: datetime
