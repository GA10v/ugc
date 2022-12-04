import typing

from services.transformer.layer_models import EventKafka, events


class TransformerProtocol(typing.Protocol):
    def transform(data: list[EventKafka]) -> dict[str, list[events]]:
        """Подготовка данных для записи."""
        ...
