import typing


class ProducerProtocol(typing.Protocol):
    async def produce(self, *args, **kwargs):
        ...

    async def batch_produce(self, *args, **kwargs):
        ...
