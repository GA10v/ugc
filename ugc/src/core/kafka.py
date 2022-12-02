from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

producer = AIOKafkaProducer
consumer = AIOKafkaConsumer


async def get_producer(*args, **kwargs) -> producer:
    return producer(*args, **kwargs)


async def get_consumer(*args, **kwargs) -> consumer:
    return consumer(*args, **kwargs)
