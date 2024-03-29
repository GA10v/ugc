import typing
from typing import Optional

from kafka import KafkaConsumer


class ExtracterProtocol(typing.Protocol):
    def _get_consumer(self) -> Optional[KafkaConsumer]:
        """Реализация отказоустойчивости."""
        ...
