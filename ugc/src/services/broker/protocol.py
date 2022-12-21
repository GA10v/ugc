import typing
from abc import abstractmethod


class ProducerProtocol(typing.Protocol):
    @abstractmethod
    async def produce(self, *args, **kwargs):
        ...

    @abstractmethod
    async def batch_produce(self, *args, **kwargs):
        ...
