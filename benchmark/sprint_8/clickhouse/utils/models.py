from datetime import datetime
from typing import TypedDict


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
