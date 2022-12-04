import backoff
from confluent_kafka import Consumer, KafkaError

from services.extracter.protocol import ExtracterProtocol


class KafkaConsumerETL(ExtracterProtocol):
    def __init__(
        self,
        host: str,
        topics: list[str],
        group_id: str,
        batch_size: int,
    ) -> None:
        self.conf = {
            'bootstrap.servers': host,
            'group.id': group_id,
            'auto.offset.reset': 'earliest',
        }
        self.topics = topics
        self.batch_size = batch_size
        self.consumer = self._get_consumer()

    @backoff.on_exception(backoff.expo, KafkaError)
    def get_consumer(self) -> Consumer:
        """Реализация отказоустойчивости."""
        return Consumer(self.conf)
