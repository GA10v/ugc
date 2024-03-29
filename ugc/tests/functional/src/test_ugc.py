from http import HTTPStatus

import pytest
from config import settings

pytestmark = pytest.mark.asyncio


async def test_producer_unauthorized(session, movie_id, event_type, event):
    """Проверка доступа неавторизованного пользователя к эндпоинту загрузки единичного события"""

    url = f'{settings.fastapi.service_url}{settings.fastapi.EVENT_PREFIX}/produce/{movie_id}/{event_type}'
    params = {'event': event}

    async with session.post(url, params=params) as response:
        assert response.status == HTTPStatus.FORBIDDEN


async def test_producer_authorized(session, access_token, movie_id, event_type, event):
    """Проверка выполнения загрузки единичного события авторизованного пользователя"""

    url = f'{settings.fastapi.service_url}{settings.fastapi.EVENT_PREFIX}/produce/{movie_id}/{event_type}'
    params = {'event': event}
    headers = {'Authorization': 'Bearer ' + access_token}

    async with session.post(url, params=params, headers=headers) as response:
        assert response.status == HTTPStatus.OK


async def test_batch_producer_unauthorized(session, movie_id, event_type, event):
    """Проверка доступа неавторизованного пользователя к эндпоинту загрузки пакета событий"""

    url = f'{settings.fastapi.service_url}{settings.fastapi.EVENT_PREFIX}/batch-produce'
    params = {'batch_size': 100}

    async with session.post(url, params=params) as response:
        assert response.status == HTTPStatus.FORBIDDEN


async def test_batch_producer_authorized(session, access_token, movie_id, event_type, event):
    """Проверка выполнения загрузки пакета событий авторизованным пользователем"""

    url = f'{settings.fastapi.service_url}{settings.fastapi.EVENT_PREFIX}/batch-produce'
    headers = {'Authorization': 'Bearer ' + access_token}
    params = {'batch_size': 100}

    async with session.post(url, params=params, headers=headers) as response:
        assert response.status == HTTPStatus.OK
