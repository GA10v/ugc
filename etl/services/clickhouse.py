import backoff
from clickhouse_driver import Client, errors
from core.config import settings
from core.logger import get_logger

logger = get_logger(__name__)


class ClickHouseClientETL:
    def __init__(
        self,
        host: str,
        port: int,
        sub: list[int],
        db: str,
        tables: list[str],
        fields: dict[str, str],
        cluster: str = 'company_cluster',
    ) -> None:
        self.host = host  # HOST
        self.port = port  # MASTER_PORT
        self.sub = sub  # SUB_PORTS
        self.cluster = cluster
        self.db = db
        self.tables = tables
        self.fields = fields
        self.databases = settings.ch.databases
        self.client = Client(host, port)

    @backoff.on_exception(backoff.expo, errors.Error)
    def _get_client(self, host: str, port: str | int) -> Client:
        """Реализация отказоустойчивости."""

        return Client(host, port)

    def _execute(self, command: str, client: Client, values=None) -> None:
        """Запрос в ClickHouse."""

        try:
            return client.execute(command, values)
        except errors.ServerException as ex:
            if ex.code != 57:
                raise ex

    def _create_db(self, db: str, client: Client) -> None:
        """Создание БД."""

        command = f'CREATE DATABASE IF NOT EXISTS {db} ON CLUSTER {self.cluster}'
        self._execute(command, client)

    def _create_distributed_table(self, table: str, client: Client) -> None:
        """Создание дистрибутивной таблицы."""

        _fields = ', '.join([f'{key} {value}' for key, value in self.fields.items()])
        command = f"""
            CREATE TABLE IF NOT EXISTS default.{table} ON CLUSTER {self.cluster} ({_fields})
            ENGINE = Distributed({self.cluster}, '', {table}, rand())
            """
        self._execute(command, client)

    def _create_replicated_tables(self, shard: str, replica: str, table: str, client: Client) -> None:
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

        self._execute(shard_command, client)
        self._execute(replica_command, client)

    def init_db(self) -> None:
        """Создание БД и Таблиц."""

        # на весь кластер:
        self._create_db(self.db, self.client)
        for db in self.databases:
            self._create_db(db, self.client)
        for table in self.tables:
            self._create_distributed_table(table, self.client)

        #  1 нода:
        client = self._get_client(self.host, self.port)
        for table in self.tables:
            self._create_replicated_tables(
                shard=self.databases[0],
                replica=self.databases[2],
                table=table,
                client=client,
            )

        #  3 нода:
        client = self._get_client(self.host, self.sub[0])
        for table in self.tables:
            self._create_replicated_tables(
                shard=self.databases[1],
                replica=self.databases[0],
                table=table,
                client=client,
            )

        #  5 нода:
        client = self._get_client(self.host, self.sub[1])
        for table in self.tables:

            self._create_replicated_tables(
                shard=self.databases[2],
                replica=self.databases[1],
                table=table,
                client=client,
            )

    def load(self, data: list) -> None:
        """Вставка данных в таблицу."""
        ...
