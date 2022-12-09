from typing import Protocol

from db.mongo import MongoRepository


class Repository(Protocol):
    async def add(self, *args, **kwargs):
        ...

    async def update(self, *args, **kwargs):
        ...

    async def delete(self, *args, **kwargs):
        ...

    async def get(self, *args, **kwargs):
        ...

    async def get_multi(self, *args, **kwargs):
        ...


database: Repository = MongoRepository()


async def get_repository() -> Repository:
    return database
