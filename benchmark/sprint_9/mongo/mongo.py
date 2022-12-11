
from pymongo import MongoClient
from utils.base_benchmark import AbsEventStorage, BaseBenchmark
from utils.settings import settings



class MongoStorage(AbsEventStorage):
    def __init__(self):
        client = MongoClient(settings.mongo.url)[settings.mongo.DATABASE]
        self.collection = client.get_collection(settings.mongo.COLLECTION)


    def insert_bath(self, data: list) -> None:
        self.collection.insert_many(data)

    def select_movie(self, movie_id: str) -> None:
        film = self.collection.find_one({'movie_id': movie_id})
        print(film)

    def get_number_record(self, movie_id: str) -> int:
        return len([film for film in self.collection.find({'movie_id': movie_id})])

    def clear_records(self) -> None:
        self.collection.drop()


if __name__ == '__main__':
    storage = MongoStorage()
    benchmark = BaseBenchmark(storage)

    # Tecт 1: Тестирование вставки данных о событиях с разным размером батча. (нет записей в таблице)
    benchmark.test_insert(1)
    benchmark.test_insert(10)
    benchmark.test_insert(100)
    benchmark.test_insert(1000)
    benchmark.test_insert(10000)

    # Tecт 2: Тестирование поиска данных о событиях. (< 15_000 записей в таблице)

    benchmark.insert_searchable_data()
    benchmark.test_select(storage)

    # Tecт 3: Тестирование вставки батча в 1_000_000 записей. (< 15_000 записей в таблице).
    benchmark.test_insert(1000000)

    # Tecт 4: Тестирование вставки данных о событиях с разным размером батча. (1_000_000 записей в таблице).
    benchmark.test_insert(1)
    benchmark.test_insert(10)
    benchmark.test_insert(100)
    benchmark.test_insert(1000)
    benchmark.test_insert(10000)

    # Тест 5: Тестирование поиска данных о событиях. (1_000_000 записей в таблице)
    benchmark.test_select(storage)

    # Тест 6: Тестирование обновления данных о событиях. (1_000_000 записей в таблице)
    benchmark.test_select_with_update(storage)
