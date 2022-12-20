from datetime import datetime

from pydantic import BaseModel


class Review(BaseModel):
    id: str
    movie_id: str
    text: str
    author_id: str
    pub_date: datetime
    likes: list[str]
    dislikes: list[str]
    author_score: int
