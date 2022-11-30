import asyncio
from contextlib import asynccontextmanager
from uuid import UUID

from aiokafka import AIOKafkaConsumer
from pydantic import BaseModel


class ViewsMessage(BaseModel):
    user_id: UUID
    film_id: UUID
    timestamp: int


class KafkaClientETL:

    def __init__(
            self,
            host,
            topics,
            group_id,
            batch_size,
    ):
        self.client = AIOKafkaConsumer(
            *topics,
            bootstrap_servers=host,
            group_id=group_id,
            auto_offset_reset='earliest',
            enable_auto_commit=False
        )
        self.batch_size = batch_size

    @staticmethod
    def _transform_to_message(record):
        key = record.key.decode()
        value = record.value.decode()
        user_id, film_id = key.split(':')
        timestamp = value
        return ViewsMessage(
            user_id=user_id,
            film_id=film_id,
            timestamp=timestamp
        )

    @asynccontextmanager
    async def connect(self):
        await self.client.start()
        yield
        await self.client.stop()

    async def _extract_data(self):
        data = await self.client.getmany(timeout_ms=5, max_records=self.batch_size)
        records = []
        for topic, topic_records in data.items():
            records.extend(topic_records)
        return records

    async def get_messages(self):
        while True:
            batch = await self._extract_data()
            msgs = []
            if not batch:
                return
            for record in batch:
                msgs.append(self._transform_to_message(record))
            yield msgs


async def main():
    kafka_client = KafkaClientETL(
        host='localhost:29092',
        topics=['views'],
        group_id='gid',
        batch_size=4
    )
    async with kafka_client.connect():
        async for msg_batch in kafka_client.get_messages():
            print(msg_batch)


if __name__ == '__main__':
    asyncio.run(main())

