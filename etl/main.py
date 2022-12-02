import json
import sys
from time import sleep

from confluent_kafka import KafkaError, KafkaException
from core.config import settings
from models.event import EventKafka
from services.extracter.consumer import KafkaConsumerETL
from services.loader.ch_client import ClickHouseClientETL
from services.transformer.transformer import TramsformerETL

client = ClickHouseClientETL(**settings.ch.client_conf)
consumer = KafkaConsumerETL(**settings.kafka.consumer_conf)
transformer = TramsformerETL()
running = True
sleep_time = 5


def main(consumer: KafkaConsumerETL, client: ClickHouseClientETL, transformer: TramsformerETL):
    try:
        consumer.get_consumer().subscribe(consumer.topics)

        while running:
            messages = consumer.consume(num_messages=100, timeout=1.0)
            if messages is None:
                continue

            events: list[EventKafka] = []
            for message in messages:
                if message.error():
                    if message.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        sys.stderr.write(
                            '%% %s [%d] reached end at offset %d\n'
                            % (message.topic(), message.partition(), message.offset()),
                        )
                    elif message.error():
                        raise KafkaException(message.error())

                events.append(EventKafka(**json.loads(message.value())))

            if events:
                events = transformer.transform(events)
                client.load(events)

            sleep(sleep_time)
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


def shutdown():
    global running
    running = False


if __name__ == '__main__':
    client.init_db()
    main(consumer, client, transformer)
