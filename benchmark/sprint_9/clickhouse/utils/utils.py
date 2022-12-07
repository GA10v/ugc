import time
from datetime import datetime
from random import choice, randint
from uuid import uuid4

from utils.clickhouse import ClickhouseClient
from utils.models import MovieRating
from utils.settings import settings


def _get_fake_event(user_id: str = None, movie_id: str = None) -> MovieRating:
    """
    Генератор фейковых событий.
    :param user_id: UUID пользователя
    :param movie_id: UUID фильма
    :return: MovieRating
    """
    _event = {
        'user_id': user_id if user_id else str(uuid4()),
        'movie_id': movie_id if movie_id else str(uuid4()),
        'rating': randint(1, 10),
        'event_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    return MovieRating(**_event).dict()


def get_fake_batch(
    batch_size: int = 10000,
    movie_size: int = 10,
    is_search: bool = False,
) -> list[MovieRating]:
    """
    Генератор батча фейковых событий.
    :param batch_size: размер батча
    :param user_size: UUID фильма
    :param movie_size: UUID фильма
    :param is_stress_test: флаг для добавления событий с известным movie_id
    :return: list[Event]
    """
    movies = [str(uuid4()) for _ in range(movie_size)]
    if is_search:
        movies = [settings.test_data.UUID]

    return [_get_fake_event(user_id=str(uuid4()), movie_id=choice(movies)) for _ in range(batch_size)]


def _insert_batch(client: ClickhouseClient, batch_size: int, table_name: str = settings.test_data.TABLE) -> None:
    """
    Тест записи данных.
    :param client: ClickhouseClient
    :param table_name: название таблицы
    :param batch_size: размер батча
    """

    data = get_fake_batch(batch_size=batch_size)
    start = time.time()
    client.insert(table_name=table_name, data=data)
    end = time.time()
    benchmark = end - start

    print('====' * 10)
    print(f'- Batch size: {batch_size} items; \n- Benchmark: {benchmark} sec.')


def test_insert_batch(client: ClickhouseClient, table_name: str = settings.test_data.TABLE) -> None:
    """
    Тест записи данных с разными размерами батча.
    :param client: ClickhouseClient
    :param table_name: название таблицы
    """

    batch_sizes = settings.test_data.BATCHES
    for batch_size in batch_sizes:
        _insert_batch(client=client, batch_size=batch_size,
                      table_name=table_name)

    # Добавление событий с известным movie_id для поиска
    data = get_fake_batch(batch_size=100, is_search=True)
    client.insert(table_name=table_name, data=data)


def stress_test_insert(client: ClickhouseClient, table_name: str = settings.test_data.TABLE):
    """
    Тест записи батча c 1_000_000 событий.
    :param client: ClickhouseClient
    :param table_name: название таблицы
    """

    batch_size = settings.test_data.STRESS_SIZE
    data = get_fake_batch(batch_size=batch_size)
    start = time.time()
    client.insert(table_name=table_name, data=data)
    end = time.time()
    benchmark = end - start

    print('====' * 10)
    print(f'- batch_size: {batch_size} items; \n- Benchmark: {benchmark} sec.')


def test_select(client: ClickhouseClient, movie_id: str, table_name: str = settings.test_data.TABLE, is_update: bool = False) -> None:
    """
    Тест поиска записей.
    :param client: ClickhouseClient
    :param movie_id: UUID фильма для поиска
    :param table_name: название таблицы
    """

    def _get_response(movie_id: str, data: list[tuple[str, int]]) -> dict:
        _count = len(data)
        likes = []
        dislikes = []
        for user, rating in data:
            if rating >= 5:
                likes.append(user)
            else:
                dislikes.append(user)
        return {
            'movie_id': movie_id,
            'likes': likes,
            'dislikes': dislikes,
            'rating': len(likes)*10/_count,
            'count': _count
        }

    def _get_data():
        return client.select(
            table_name=table_name,
            fields=['user_id', 'rating'],
            movie_id=movie_id,
        )
    
    start = time.time()
    data = _get_data()
    res = _get_response(movie_id=movie_id, data=data)
    start_count = res['count']
    if is_update:
        _data = get_fake_batch(batch_size=100, is_search=True)
        client.insert(table_name=table_name, data=_data)
        data = _get_data()
        while res['count'] < start_count:
            data = _get_data()
            res = _get_response(movie_id=movie_id, data=data)
    
    end = time.time()
    benchmark = end - start

    records = client.client.execute(f'SELECT COUNT(*) from {table_name}')[0][0]
    print(res)
    print('====' * 10)
    print(f'- Records: {records} items; \n- Benchmark: {benchmark} sec.')
