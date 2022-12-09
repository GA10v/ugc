from db.repository import Repository


class MongoRepository(Repository):
    def __init__(self, client):
        self.client = client

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
