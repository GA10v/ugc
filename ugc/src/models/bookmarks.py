from random import choices, randint
from uuid import uuid4

from models.base import BaseOrjsonModel


class BookmarksSchema(BaseOrjsonModel):
    user_id: str
    bookmarks: list[str]

    class Config:
        schema_extra = {
            'example': {
                'user_id': '4796fe00-fe9c-4def-a471-a9a4d448b60d',
                'bookmarks': [
                    '8f092fcd-1744-464f-a783-d9a6c4ec59d5',
                    '5da55e02-e760-4687-a07a-e440d1ec5552',
                    'dcaf8556-8aba-4811-8ec8-365982b30b8c',
                    '4b090a3d-075d-49c4-b8f4-db4689478240',
                    'b92943d2-2030-449b-8cc9-00fb26c73428',
                ],
            },
        }


def _get_fake_event(user_id: str = None, bookmarks: list[str] = None, bm_size: int = 5) -> BookmarksSchema:
    """
    Генератор фейковых событий.
    :param user_id: UUID пользователя
    :param bookmarks: список UUID фильмов
    :param bm_size: количество подписок пользователя
    :return: UserBookmarks
    """
    _event = {
        'user_id': user_id if user_id else str(uuid4()),
        'bookmarks': bookmarks if bookmarks else [str(uuid4()) for _ in range(bm_size)],
    }
    return BookmarksSchema(**_event)


def get_fake_batch(batch_size: int = 10000, movies_size: int = 1000) -> list[BookmarksSchema]:
    users = [str(uuid4()) for _ in range(batch_size)]
    movies = [str(uuid4()) for _ in range(movies_size)]
    bm_count = randint(1, movies_size)
    return [_get_fake_event(user_id=users[_], bookmarks=choices(movies, k=bm_count)) for _ in range(len(users))]
