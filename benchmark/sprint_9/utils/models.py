from datetime import datetime

from pydantic import BaseModel


class MovieRating(BaseModel):

    user_id: str
    movie_id: str
    rating: int
    event_time: datetime
