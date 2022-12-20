from datetime import datetime

import backoff
from clickhouse_driver import Client, errors
from core.config import settings
from core.logger import get_logger
from models.event import events
from services.loader.protocol import LoaderProtocol

logger = get_logger(__name__)


class ClickHouseClientETL(LoaderProtocol):
    def __init__(
        self,
        host: str,
        port: int,
        db: str,
        tables: list[str],
        fields: dict[str, str],
        cluster: str = 'company_cluster',
    ) -> None:
        self.host = host  # HOST
        self.port = port  # MASTER_PORT
        self.cluster = cluster
        self.db = db
        self.tables = tables
        self.fields = fields
        self.databases = settings.ch._databases
        self.client = self._get_client()

    @backoff.on_exception(backoff.expo, errors.Error)
    def _get_client(self) -> Client:
        """Реализация отказоустойчивости."""

        return Client(self.host, self.port)

    def _execute(self, command: str, values=None) -> None:
        """
        Запрос в ClickHouse.
        :param command: Запрос в ClickHouse
        :param values: Данные для встаки в запрос
        :raises ServerException:
        """

        try:
            return self.client.execute(command, values)
        except errors.ServerException as ex:
            if ex.code != 57:
                logger.error('ClickHouse: bad request \n %s', str(ex))
                raise ex

    def _create_db(self, db: str) -> None:
        """Создание БД в ClickHouse."""

        command = f'CREATE DATABASE IF NOT EXISTS {db} ON CLUSTER {self.cluster}'
        self._execute(command)

    def _create_distributed_table(self, table: str) -> None:
        """Создание дистрибутивной таблицы."""

        _fields = ', '.join([f'{key} {value}' for key, value in self.fields.items()])
        command = f"""
            CREATE TABLE IF NOT EXISTS default.{table} ON CLUSTER {self.cluster} ({_fields})
            ENGINE = Distributed({self.cluster}, '', {table}, rand())
            """
        self._execute(command)

    def _create_replicated_tables(self, shard: str, replica: str, table: str) -> None:
        """Создание реплицированных таблиц."""

        _fields = ', '.join([f'{key} {value}' for key, value in self.fields.items()])
        shard_command = f"""
            CREATE TABLE IF NOT EXISTS {shard}.{table} ({_fields})
            ENGINE = ReplicatedMergeTree('/clickhouse/tables/{{shard01}}/{table}', '{{replica01}}')
            ORDER BY event_time
            """
        replica_command = f"""
            CREATE TABLE IF NOT EXISTS {replica}.{table} ({_fields})
            ENGINE = ReplicatedMergeTree('/clickhouse/tables/{{shard02}}/{table}', '{{replica02}}')
            ORDER BY event_time
            """

        self._execute(shard_command)
        self._execute(replica_command)

    @staticmethod
    def _correct_insert_values(item) -> str:
        """Приведение значений item к строке перед записью в таблицу."""

        if isinstance(item, datetime):
            return f"toDateTime('{item}')"
        if isinstance(item, int):
            return str(item)
        return f"'{item}'"

    def init_db(self) -> None:
        """Создание БД и Таблиц в ClickHouse."""

        logger.info('Cluster: init db')
        self._create_db(self.db)
        for db in self.databases:
            self._create_db(db)
        for table in self.tables:
            self._create_distributed_table(table)

    def load(self, data: dict[str, list[events]]) -> None:
        """
        Вставка данных в ClickHouse.
        :param data: Подготовенный батч данных
        """

        for event_type, batch in data.items():
            try:
                _fields = list(batch[0].keys())
            except IndexError:
                continue
            _values = []
            for item in batch:
                row = ', '.join([self._correct_insert_values(item.get(field)) for field in _fields])
                _values.append(f'({row})')
            fields = ', '.join(_fields)
            values = ', '.join(_values)
            self._execute(f'INSERT INTO {self.db}.{event_type} ({fields}) VALUES {values}')
            logger.info('ClickHouse: event [%s] loaded', event_type)
