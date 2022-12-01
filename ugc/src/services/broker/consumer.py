from services.broker.protocol import ConsumerProtocol


class KafkaConsumer(ConsumerProtocol):
    ...


consumer: KafkaConsumer = KafkaConsumer()


async def get_consumer() -> consumer:
    return consumer
