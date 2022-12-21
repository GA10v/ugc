from http import HTTPStatus

import pytest
from config import settings

pytestmark = pytest.mark.asyncio


@pytest.fixture
def data_one_bm():
    return {
        'user_id': settings.data.USER,
        'bookmarks': [settings.data.MOVIE_1],
    }


@pytest.fixture
def data_two_bm():
    return {
        'user_id': settings.data.USER,
        'bookmarks': [settings.data.MOVIE_1, settings.data.MOVIE_2],
    }


async def test_get_unauthorized(session):
    """Проверка доступа неавторизованного пользователя."""
    _url = f'{settings.fastapi.service_url}{settings.fastapi.BOOKMARK_PREFIX}/'
    url = _url + settings.data.USER
    async with session.get(url) as response:
        assert response.status == HTTPStatus.FORBIDDEN


async def test_get_not_found(session, access_token):
    """Проверка поиска по несуществующему id."""
    _url = f'{settings.fastapi.service_url}{settings.fastapi.BOOKMARK_PREFIX}/'
    headers = {'Authorization': 'Bearer ' + access_token}

    url = _url + 'wrong_user_id'
    async with session.get(url, headers=headers) as response:
        assert response.status == HTTPStatus.NOT_FOUND


async def test_add_ok(session, access_token, data_one_bm, data_two_bm):
    """Проверка добавления закладок."""
    _url = f'{settings.fastapi.service_url}{settings.fastapi.BOOKMARK_PREFIX}/'
    headers = {'Authorization': 'Bearer ' + access_token}

    url = _url + settings.data.MOVIE_1
    async with session.post(url, headers=headers) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert body == data_one_bm

    url = _url + settings.data.MOVIE_2
    async with session.post(url, headers=headers) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert body == data_two_bm


async def test_delete_not_found(session, access_token, data_one_bm):
    """Проверка удаления закладок по несуществующему id."""
    _url = f'{settings.fastapi.service_url}{settings.fastapi.BOOKMARK_PREFIX}/'
    headers = {'Authorization': 'Bearer ' + access_token}

    url = _url + 'wrong_movie_id'
    async with session.delete(url, headers=headers) as response:
        assert response.status == HTTPStatus.NOT_FOUND


async def test_delete_ok(session, access_token, data_one_bm):
    """Проверка удаления закладок."""
    _url = f'{settings.fastapi.service_url}{settings.fastapi.BOOKMARK_PREFIX}/'
    headers = {'Authorization': 'Bearer ' + access_token}

    url = _url + settings.data.MOVIE_2
    async with session.delete(url, headers=headers) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert body == data_one_bm


async def test_get_ok(session, access_token, data_one_bm):
    """Проверка получения закладок."""
    _url = f'{settings.fastapi.service_url}{settings.fastapi.BOOKMARK_PREFIX}/'
    headers = {'Authorization': 'Bearer ' + access_token}

    url = _url + settings.data.USER
    async with session.get(url, headers=headers) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert body == data_one_bm

    # Удаление тестовых данных
    _url = f'{settings.fastapi.service_url}{settings.fastapi.BOOKMARK_PREFIX}/'
    url = _url + settings.data.MOVIE_1
    async with session.delete(url, headers=headers) as response:
        assert response.status == HTTPStatus.OK
