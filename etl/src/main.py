import gc
import json
import sys
from time import sleep

from confluent_kafka import KafkaError, KafkaException

from core.config import settings
from models.event import EventKafka, RatingEvent, ViewsEvent
from services.extracter.consumer import KafkaConsumerETL
from services.loader.ch_client import ClickHouseClientETL
from services.transformer.transformer import TramsformerETL

client = ClickHouseClientETL(**settings.ch.client_conf)
consumer = KafkaConsumerETL(**settings.kafka.consumer_conf)
transformer = TramsformerETL()
running = True
sleep_time = 2


def main(consumer: KafkaConsumerETL, client: ClickHouseClientETL, transformer: TramsformerETL):
    try:
        _consumer = consumer.get_consumer()
        _consumer.subscribe(consumer.topics)

        while running:
            messages = _consumer.consume(num_messages=100, timeout=1.0)
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

                _event = json.loads(message.value())
                event_type = _event.get('event_type')

                if event_type == 'rating':
                    event_payload = RatingEvent(**_event.get('event_payload'))
                if event_type == 'views':
                    event_payload = ViewsEvent(**_event.get('event_payload'))

                events.append(EventKafka(event_type=event_type, event_payload=event_payload))

            if events:
                events = transformer.transform(events)
                client.load(events)
                _consumer.commit(asynchronous=False)

            gc.collect()
            sleep(sleep_time)
    finally:
        # Close down consumer to commit final offsets.
        _consumer.close()


def shutdown():
    global running
    running = False


if __name__ == '__main__':
    client.init_db()
    main(consumer, client, transformer)
