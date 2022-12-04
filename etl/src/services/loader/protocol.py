import typing
from typing import Optional

from clickhouse_driver import Client

from services.loader.layer_models import events


class LoaderProtocol(typing.Protocol):
    def _get_client(self) -> Optional[Client]:
        """Реализация отказоустойчивости."""
        ...

    def init_db(self) -> None:
        """Создание БД и Таблиц в ClickHouse."""
        ...

    def load(self, data: dict[str, list[events]]) -> None:
        """Вставка данных в ClickHouse."""
        ...
