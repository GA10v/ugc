from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Event(BaseModel):
    user_id: UUID  # надо узнать что приходит из transform UUID | str
    movie_id: UUID  # надо узнать что приходит из transform UUID | str
    evetn: int
    event_time: datetime  # надо узнать что приходит из transform datetime | str

    @property
    def dict(self) -> dict:
        _dict = super().dict()
        _dict['user_id'] = str(_dict['user_id'])  # удалить если приходит str
        _dict['movie_id'] = str(_dict['movie_id'])  # удалить если приходит str
        _dict['event_time'] = _dict['movie_id'].strftime('%Y-%m-%d %H:%M:%S')  # удалить если приходит str
        return _dict
