from pydantic import BaseModel


class UserRating(BaseModel):
    user_id: str
    rating: int


class Rating(BaseModel):
    movie_id: str
    data: list[UserRating]


class Likes(BaseModel):
    movie_id: str
    likes: list[str]
    dislikes: list[str]
    rating: float
