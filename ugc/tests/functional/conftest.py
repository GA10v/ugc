import asyncio
import uuid
from random import choice, randint

import aiohttp
import jwt
import pytest_asyncio
from config import settings


@pytest_asyncio.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
def access_token():
    data = {'sub': settings.data.USER, 'permissions': [], 'is_super': True}
    return jwt.encode(data, settings.jwt.SECRET_KEY, settings.jwt.ALGORITHM)


@pytest_asyncio.fixture(scope='session')
def movie_id():
    return str(uuid.uuid4())


@pytest_asyncio.fixture(scope='session')
def event_type():
    return choice(settings.kafka.TOPICS)


@pytest_asyncio.fixture(scope='session')
def event():
    return randint(1, 10000)
