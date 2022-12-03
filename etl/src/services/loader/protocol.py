import typing
from typing import Optional

from clickhouse_driver import Client


class LoaderProtocol(typing.Protocol):
    def _get_client(self) -> Optional[Client]:
        """Реализация отказоустойчивости."""
        ...

    def init_db(self) -> None:
        """Создание БД и Таблиц в ClickHouse."""
        ...

    def load(self) -> None:
        """Вставка данных в ClickHouse."""
        ...
