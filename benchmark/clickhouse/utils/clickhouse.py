from datetime import datetime

from clickhouse_driver import Client
from utils.models import Event
from utils.settings import settings


class ClickhouseClient:
    def __init__(self, host: str) -> None:
        self.client = Client(host=host)

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

    def create_db(self, name: str, cluster: str) -> None:
        """
        Создание БД.
        :param name: название БД
        :param cluster: название кластера
        """

        command = f'CREATE DATABASE IF NOT EXISTS {name} ON CLUSTER {cluster}'
        self.client.execute(command)

    def create_replicated_table(
        self,
        table_name: str,
        fields: dict[str, str] = settings.fields.FIELDS,
        cluster: str = settings.clickhouse.CLUSTER_NAME,
        partition_by: str = settings.fields.PARTITION,
        order_by: str = settings.fields.ORDER,
    ) -> None:
        """Создание реплицированной таблицы."""

        self._create_table(
            table_name=table_name,
            fields=fields,
            cluster=cluster,
            engine=f"ReplicatedMergeTree('/clickhouse/tables/{{shard}}/{table_name}', '{{replica}}')",
            partition_by=partition_by,
            order_by=order_by,
        )

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

    def insert(self, table_name: str, data: list[Event]) -> None:
        """
        Вставка данных в таблицу
        :param table_name: название таблицы
        :param data: сипсок событий
        """

        _fields = list(data[0].keys())
        _values = []
        for item in data:
            row = ', '.join([self._correct_insert_values(item.get(field)) for field in _fields])
            _values.append(f'({row})')

        fields = ', '.join(_fields)
        values = ', '.join(_values)
        command = f'INSERT INTO {table_name} ({fields}) VALUES {values}'

        self.client.execute(command)

    def select(self, table_name: str, fields: list[str] = None, movie_id: str = None) -> list:
        """
        Получение данных из таблицы.
        :param table_name: название таблицы
        :param data: сипсок событий
        param movie_id: UUID
        """

        if fields:
            fields = ', '.join(fields)
        else:
            fields = '*'
        command = f'SELECT {fields} FROM {table_name}'

        if movie_id:
            command += f" WHERE movie_id = '{movie_id}'"

        return self.client.execute(command)
