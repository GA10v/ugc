from pydantic import BaseModel
from datetime import datetime


class MovieRating(BaseModel):

    user_id: str
    movie_id: str
    rating: int
    event_time: datetime
