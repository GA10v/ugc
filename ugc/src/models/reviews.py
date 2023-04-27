from datetime import datetime
from typing import Optional

from pydantic import Field

from .base import BaseOrjsonModel


class ReviewSchema(BaseOrjsonModel):
    id: str  # noqa: VNE003
    movie_id: str
    text: str
    author_id: str
    pub_date: datetime
    likes: list[str]
    dislikes: list[str]

    class Config:
        schema_extra = {
            'example': {
                'id': '63a0da94e5601a0591009388',
                'movie_id': '5da55e02-e760-4687-a07a-e440d1ec5552',
                'text': 'There’s little of Tolkien in this ‘Tolkien epic’. '
                'The acting is dire and even laughable throughout. '
                'The story, or lack thereof, is a convoluted, nonsensical mess. '
                'The characters have been butchered and are now rendered unlikable and unrecognisable',
                'author_id': 'a3ec68e8-c972-456c-80ab-c737fb21c6e4',
                'pub_date': '2022-12-19T21:41:40.322+00:00',
                'likes': [
                    '067b457b-05ce-4fbb-9388-407f0c578916',
                    '9580c371-54b2-410d-8250-a29520669ea6',
                    '99bdf6ab-d698-4264-8ab1-950ef14dc85a',
                ],
                'dislike': ['60a8144f-7e21-4678-b1f0-d8a1ac8955e0'],
            },
        }


class ReviewResponse(BaseOrjsonModel):
    id: str = Field(description='ID рецензии', default='id_for_validate')  # noqa: VNE003
    movie_id: str = Field(description='ID фильма рецензии')
    text: str = Field(description='Текст рецензии')
    author_id: str = Field(description='ID пользователя, написавшего рецензию')
    pub_date: datetime = Field(description='Дата добавления рецензии', default_factory=datetime.today)
    likes: list[str] = Field(description='Список ID пользователей, добавивших лайк рецензии', default_factory=list)
    dislikes: list[str] = Field(
        description='Список ID пользователей, добавивших дизлайк рецензии',
        default_factory=list,
    )
    author_score: Optional[int] = Field(description='Авторская оценка фильму', default=None)

    class Config:
        schema_extra = {
            'example': {
                'id': '63a0da94e5601a0591009388',
                'movie_id': '5da55e02-e760-4687-a07a-e440d1ec5552',
                'text': 'There’s little of Tolkien in this ‘Tolkien epic’. '
                'The acting is dire and even laughable throughout. '
                'The story, or lack thereof, is a convoluted, nonsensical mess. '
                'The characters have been butchered and are now rendered unlikable and unrecognisable',
                'author_id': 'a3ec68e8-c972-456c-80ab-c737fb21c6e4',
                'pub_date': '2022-12-19T21:41:40.322+00:00',
                'likes': [
                    '067b457b-05ce-4fbb-9388-407f0c578916',
                    '9580c371-54b2-410d-8250-a29520669ea6',
                    '99bdf6ab-d698-4264-8ab1-950ef14dc85a',
                ],
                'dislike': ['60a8144f-7e21-4678-b1f0-d8a1ac8955e0'],
                'author_score': 3,
            },
        }
