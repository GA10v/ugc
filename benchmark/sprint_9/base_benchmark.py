from abc import ABC, abstractmethod
from datetime import datetime
from random import choice, randint
from uuid import UUID, uuid4

from clickhouse.utils.decorators import timer
from clickhouse.utils.models import MovieRating
from clickhouse.utils.settings import settings


class AbsEventStorage(ABC):
    @abstractmethod
    def insert_bath(self, data: list) -> None:
        ...

    @abstractmethod
    def select_movie(self, movie_id: UUID) -> None:
        ...

    @abstractmethod
    def get_number_record(self, movie_id: UUID) -> int:
        ...

    @abstractmethod
    def clear_records(self) -> None:
        ...


class BaseBenchmark:
    def __init__(self, storage: AbsEventStorage):
        self.storage = storage
        self.storage.clear_records()

    @staticmethod
    def _get_fake_event(user_id: str = None, movie_id: str = None) -> MovieRating.dict:
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

    @staticmethod
    def _generate_searchable_data() -> [MovieRating.dict]:
        _event = {
            'user_id': str(uuid4()),
            'movie_id': settings.test_data.UUID,
            'rating': randint(1, 10),
            'event_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        return [MovieRating(**_event).dict()]

    @classmethod
    def _generate_test_data(cls, batch_size: int) -> list[MovieRating.dict]:
        movie_size = 10
        movies = [settings.test_data.UUID for _ in range(movie_size)]
        return [cls._get_fake_event(user_id=str(uuid4()), movie_id=choice(movies)) for _ in range(batch_size)]

    @timer('Загрузка батчами')
    def test_insert(self, batch: int, add_searchable_data: bool = False) -> None:
        fake_even_data = self._generate_test_data(batch)
        self.storage.insert_bath(fake_even_data)

        if add_searchable_data:
            fake_even_data = self._generate_searchable_data()
            self.storage.insert_bath(fake_even_data)

    @timer('Поиск фильма')
    def test_select(self, storage: AbsEventStorage) -> None:
        storage.select_movie(settings.test_data.UUID)

    @timer('Тест обновления')
    def test_select_with_update(self, storage: AbsEventStorage) -> None:
        start_record = storage.get_number_record(settings.test_data.UUID)
        fake_even_data = self._generate_test_data(100)
        storage.insert_bath(fake_even_data)
        record_count = start_record
        while record_count != start_record + 100:
            record_count = storage.get_number_record(settings.test_data.UUID)
