from datetime import datetime

from clickhouse_driver import Client
from utils.base_benchmark import AbsEventStorage
from utils.settings import settings


class CHStorage(AbsEventStorage):
    def __init__(self, host: str) -> None:
        self.client = Client(host=host)

    def insert_bath(self, data: list) -> None:
        _fields = list(data[0].keys())
        _values = []
        for item in data:
            row = ', '.join([self._correct_insert_values(item.get(field)) for field in _fields])
            _values.append(f'({row})')
        fields = ', '.join(_fields)
        values = ', '.join(_values)
        command = f'INSERT INTO {settings.test_data.TABLE} ({fields}) VALUES {values}'
        self.client.execute(command)

    def select_movie(self, movie_id: str) -> None:
        command = f"SELECT 'user_id', 'rating' FROM {settings.test_data.TABLE} WHERE movie_id = '{movie_id}'"
        return self.client.execute(command)

    def get_number_record(self, movie_id: str) -> int:
        command = f'SELECT COUNT(*) from {settings.test_data.TABLE}'
        return self.client.execute(command)[0][0]

    def clear_records(self) -> None:
        command = f'DROP TABLE IF EXISTS {settings.test_data.TABLE}'
        return self.client.execute(command)

    @staticmethod
    def _correct_insert_values(item) -> str:
        """Приведение значений item к строке перед записью в таблицу."""

        if isinstance(item, datetime):
            return f"toDateTime('{item}')"
        if isinstance(item, int):
            return str(item)
        return f"'{item}'"

    def _create_table(
        self,
        table_name: str,
        fields: dict[str, str],
        engine: str,
        cluster: str,
        partition_by: str = None,
        order_by: str = None,
    ) -> None:
        """
        Создание таблиц.
        :param table_name: название таблицы
        :param fields: название полей таблицы и их типы
        :param engine: engine таблицы
        :param cluster: название кластера
        :param partition_by: поля для партицирования
        :param order_by: поля для ключа
        """

        _fields = ', '.join([f'{key} {value}' for key, value in fields.items()])
        command = f'CREATE TABLE IF NOT EXISTS {table_name} ON CLUSTER {cluster} ({_fields}) ENGINE = {engine}'
        if partition_by:
            command += f' PARTITION BY {partition_by}'
        if order_by:
            command += f' ORDER BY {order_by}'

        self.client.execute(command)

    def create_distributed_table(
        self,
        table_name: str,
        fields: dict[str, str] = settings.fields.FIELDS,
        cluster: str = settings.clickhouse.CLUSTER_NAME,
    ) -> None:
        """Создание дистрибутивной таблицы."""

        _table_name = f'default.{table_name}'
        self._create_table(
            table_name=_table_name,
            fields=fields,
            cluster=cluster,
            engine=f"Distributed({settings.clickhouse.CLUSTER_NAME}, '', {table_name}, rand())",
        )
