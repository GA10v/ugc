import typing
from typing import Optional

from aiokafka import AIOKafkaConsumer


class ProducerProtocol(typing.Protocol):
    async def produce(self, *args, **kwargs):
        ...

    async def batch_produce(self, *args, **kwargs):
        ...


class ConsumerProtocol(typing.Protocol):
    async def connect(self, *args, **kwargs) -> Optional[AIOKafkaConsumer]:
        ...

    async def get_messages(self, *args, **kwargs) -> Optional[list]:
        ...
