import typing

from services.transformer.layer_models import events


class TransformerProtocol(typing.Protocol):
    def transform() -> dict[str, list[events]]:
        ...
