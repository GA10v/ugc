from models.base import BaseOrjsonModel
from pydantic import Field


class UserRatingSchema(BaseOrjsonModel):
    user_id: str
    rating: int = Field(ge=0, le=10)


class RatingSchema(BaseOrjsonModel):
    movie_id: str
    data: list[UserRatingSchema]

    class Config:
        schema_extra = {
            'example': {
                'movie_id': '8f092fcd-1744-464f-a783-d9a6c4ec59d5',
                'data': [
                    {
                        'user_id': '4796fe00-fe9c-4def-a471-a9a4d448b60d',
                        'rating': 6,
                    },
                    {
                        'user_id': 'dcaf8556-8aba-4811-8ec8-365982b30b8c',
                        'rating': 4,
                    },
                ],
            },
        }


class LikesResponse(BaseOrjsonModel):
    movie_id: str
    likes: list[UserRatingSchema]
    dislikes: list[UserRatingSchema]
    rating: float

    class Config:
        schema_extra = {
            'example': {
                'movie_id': '8f092fcd-1744-464f-a783-d9a6c4ec59d5',
                'likes': [
                    {
                        'user_id': '4796fe00-fe9c-4def-a471-a9a4d448b60d',
                        'rating': 6,
                    },
                ],
                'dislikes': [
                    {
                        'user_id': 'dcaf8556-8aba-4811-8ec8-365982b30b8c',
                        'rating': 4,
                    },
                ],
                'rating': 5.0,
            },
        }
