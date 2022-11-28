import time
from datetime import datetime
from random import choice, randint
from uuid import uuid4

from utils.models import Event
from utils.settings import settings
from utils.vertica import VerticaClient


def _get_fake_event(user_id: str = None, movie_id: str = None) -> Event:
    """
    Генератор фейковых событий.
    :param user_id: UUID пользователя
    :param movie_id: UUID фильма
    :return: Event
    """

    user_id = user_id if user_id else str(uuid4())
    movie_id = movie_id if movie_id else str(uuid4())
    evetn = randint(1, 180)
    event_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return Event(user_id, movie_id, evetn, event_time)


def get_fake_batch(
    batch_size: int = 10000,
    user_size: int = 100,
    movie_size: int = 1000,
    is_stress_test: bool = False,
) -> list[Event]:
    """
    Генератор батча фейковых событий.
    :param batch_size: размер батча
    :param user_size: UUID фильма
    :param movie_size: UUID фильма
    :param is_stress_test: флаг для добавления событий с известным movie_id
    :return: list[Event]
    """
    users = [str(uuid4()) for _ in range(user_size)]
    movies = [str(uuid4()) for _ in range(movie_size)]
    if is_stress_test:
        movies = [settings.test_data.UUID]

    return [_get_fake_event(user_id=choice(users), movie_id=choice(movies)) for _ in range(batch_size)]


def _insert_batch(client: VerticaClient, table_name: str, batch_size: int) -> None:
    """
    Тест записи данных.
    :param client: VerticaClient
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


def test_insert_batch(client: VerticaClient, table_name: str) -> None:
    """
    Тест записи данных с разными размерами батча.
    :param client: VerticaClient
    :param table_name: название таблицы
    """

    batch_sizes = settings.test_data.BATCHES
    for batch_size in batch_sizes:
        _insert_batch(client=client, batch_size=batch_size, table_name=table_name)

    # Добавление событий с известным movie_id для поиска
    data = get_fake_batch(batch_size=1000, is_stress_test=True)
    client.insert(table_name=table_name, data=data)


def stress_test_insert(client: VerticaClient, table_name: str):
    """
    Тест записи батча c 1_000_000 событий.
    :param client: VerticaClient
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


def test_select(client: VerticaClient, table_name: str, movie_id: str) -> None:
    """
    Тест поиска записей.
    :param client: VerticaClient
    :param table_name: название таблицы
    """

    start = time.time()
    client.select(table_name=table_name, movie_id=movie_id)
    end = time.time()
    benchmark = end - start
    with client.get_conn() as connection:
        cursor = connection.cursor()
        cursor.execute(f'SELECT COUNT(*) from {table_name}')
        records = [row for row in cursor.iterate()][0][0]

    print('====' * 10)
    print(f'- Records: {records} items; \n- Benchmark: {benchmark} sec.')
