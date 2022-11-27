from datetime import datetime
from random import choice, randint
from typing import TypedDict
from uuid import uuid4


class Event(TypedDict):
    """TypedDict"""

    user_id: str
    movie_id: str
    evetn: int
    event_time: datetime


def _get_fake_event(user_id: str = None, movie_id: str = None) -> Event:
    """
    Генератор фейковых событий.
    :param user_id: UUID пользователя
    :param movie_id: UUID фильма
    :return: Event
    """
    return {
        'user_id': user_id if user_id else str(uuid4()),
        'movie_id': movie_id if movie_id else str(uuid4()),
        'evetn': randint(1, 180),
        'event_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }


def get_fake_batch(batch_size: int = 10000, user_size: int = 100, movie_size: int = 1000) -> list[Event]:
    """
    Генератор батча фейковых событий.
    :param batch_size: размер батча
    :param user_size: UUID фильма
    :movie_size: UUID фильма
    :return: list[Event]
    """
    users = [str(uuid4()) for _ in range(user_size)]
    movies = [str(uuid4()) for _ in range(movie_size)]

    return [_get_fake_event(user_id=choice(users), movie_id=choice(movies)) for _ in range(batch_size)]
