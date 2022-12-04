from core.config import settings
from models.event import EventKafka, events
from services.transformer.protocol import TransformerProtocol


class TramsformerETL(TransformerProtocol):
    @staticmethod
    def transform(data: list[EventKafka]) -> dict[str, list[events]]:
        batches: dict = settings.transform.batches
        for item in data:
            batches[item.event_type].append(item.event_payload.dict())

        return batches
