from models.event import EventKafka, events
from services.transformer.protocol import TransformerProtocol


class TramsformerETL(TransformerProtocol):
    @staticmethod
    def transform(data: list[EventKafka]) -> dict[str, list[events]]:
        batches = {}
        for item in data:
            batches[item['event_type']].append(item['event'])

        return batches
