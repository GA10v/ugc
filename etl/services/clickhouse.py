from clickhouse_driver import Client
from core.logger import get_logger

logger = get_logger(__name__)


class ClickHouseClientETL:
    def __init__(
        self,
        host: str,
        db: str,
        tables: list[str],
        fields: dict[str, str],
        cluster: str = 'company_cluster',
    ) -> None:
        self.cluster = cluster
        self.db = db
        self.tables = tables
        self.fields = fields
        self.client = Client(host=host)

    def _create_db(self, db: str = None) -> None:
        """Создание БД."""

        if db is None:
            db = self.db
        self.client.execute(
            f'CREATE DATABASE IF NOT EXISTS {db} ON CLUSTER {self.cluster}'
        )

    def _create_distributed_table(self, table: str = None) -> None:
        """Создание дистрибутивной таблицы."""

        _fields = ', '.join([f'{key} {value}' for key, value in self.fields.items()])
        self.client.execute(
            f"""
            CREATE TABLE IF NOT EXISTS default.{table} ON CLUSTER {self.cluster} ({_fields}) 
            ENGINE = Distributed({self.cluster}, '', {table}, rand())
            """
        )

    def _create_replicated_tables(self, table: str) -> None:
        """Создание реплицированной таблицы."""

        if db is None:
            db = self.db
        _fields = ', '.join([f'{key} {value}' for key, value in self.fields.items()])
        self.client.execute(
            f"""
            CREATE TABLE IF NOT EXISTS shard.{table} ON CLUSTER {self.cluster} ({_fields}) 
            ENGINE = ReplicatedMergeTree('/clickhouse/tables/{{shard}}/{table}', '{{replica}}')
            ORDER BY event_time
            """
        )
        self.client.execute(
            f"""
            CREATE TABLE IF NOT EXISTS replica.{table} ON CLUSTER {self.cluster} ({_fields}) 
            ENGINE = ReplicatedMergeTree('/clickhouse/tables/{{shard}}/{table}', '{{replica}}')
            ORDER BY event_time
            """
        )

    def init_db(self) -> None:
        """Создание БД и Таблиц."""

        self._create_db()
        self._create_db(db='shard')
        self._create_db(db='replica')

        for table in self.tables:
            self._create_distributed_table(table)
            self._create_replicated_tables(table)

    def load(self, data: list) -> None:
        """Вставка данных в таблицу."""
        ...
