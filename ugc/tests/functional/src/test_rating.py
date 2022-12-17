from http import HTTPStatus

import jwt
import pytest
from config import settings

pytestmark = pytest.mark.asyncio


@pytest.fixture
def rating_add():
    return {
        'movie_id': settings.data.MOVIE_1,
        'data': [
            {
                'user_id': settings.data.USER,
                'rating': settings.data.RATING_1,
            },
            {
                'user_id': settings.data.USER_2,
                'rating': settings.data.RATING_2,
            },
        ],
    }


@pytest.fixture
def rating_change():
    return {
        'movie_id': settings.data.MOVIE_1,
        'data': [
            {
                'user_id': settings.data.USER,
                'rating': settings.data.RATING_2,
            },
            {
                'user_id': settings.data.USER_2,
                'rating': settings.data.RATING_2,
            },
        ],
    }


@pytest.fixture
def rating_delete():
    return {
        'movie_id': settings.data.MOVIE_1,
        'data': [
            {
                'user_id': settings.data.USER_2,
                'rating': settings.data.RATING_2,
            },
        ],
    }


@pytest.fixture
def likes():
    return {
        'movie_id': settings.data.MOVIE_1,
        'likes': [
            {
                'user_id': settings.data.USER_2,
                'rating': settings.data.RATING_2,
            },
        ],
        'dislikes': [
            {
                'user_id': settings.data.USER,
                'rating': settings.data.RATING_1,
            },
        ],
        'rating': (settings.data.RATING_1 + settings.data.RATING_2) / 2,
    }


@pytest.fixture
def access_token_user_2():
    data = {'sub': settings.data.USER_2, 'permissions': [], 'is_super': True}
    return jwt.encode(data, settings.jwt.SECRET_KEY, settings.jwt.ALGORITHM)


async def test_get_unauthorized(session):
    """Проверка доступа неавторизованного пользователя."""
    _url = f'{settings.fastapi.service_url}{settings.fastapi.RATING_PREFIX}/'
    url = _url + settings.data.MOVIE_1
    async with session.get(url) as response:
        assert response.status == HTTPStatus.FORBIDDEN


async def test_get_not_found(session, access_token):
    """Проверка поиска по несуществующему id."""
    _url = f'{settings.fastapi.service_url}{settings.fastapi.RATING_PREFIX}/'
    headers = {'Authorization': 'Bearer ' + access_token}

    url = _url + 'wrong_movie_id'
    async with session.get(url, headers=headers) as response:
        assert response.status == HTTPStatus.NOT_FOUND


async def test_add_ok(session, access_token, access_token_user_2, rating_add):
    """Проверка добавления оценки."""
    _url = f'{settings.fastapi.service_url}{settings.fastapi.RATING_PREFIX}/'
    headers_1 = {'Authorization': 'Bearer ' + access_token}
    headers_2 = {'Authorization': 'Bearer ' + access_token_user_2}
    params_1 = {'rating': settings.data.RATING_1}
    params_2 = {'rating': settings.data.RATING_2}
    url = _url + settings.data.MOVIE_1
    async with session.post(url, headers=headers_1, params=params_1) as response:
        assert response.status == HTTPStatus.OK
    async with session.post(url, headers=headers_2, params=params_2) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert body == rating_add


async def test_second_add_ok(session, access_token, rating_change):
    """Проверка добавления оценки."""
    _url = f'{settings.fastapi.service_url}{settings.fastapi.RATING_PREFIX}/'
    headers = {'Authorization': 'Bearer ' + access_token}

    url = _url + settings.data.MOVIE_1
    params = {'rating': settings.data.RATING_2}
    async with session.post(url, headers=headers, params=params) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert body == rating_change


async def test_delete_ok(session, access_token, rating_delete):
    """Проверка удаления закладок."""
    _url = f'{settings.fastapi.service_url}{settings.fastapi.RATING_PREFIX}/'
    headers = {'Authorization': 'Bearer ' + access_token}

    url = _url + settings.data.MOVIE_1
    async with session.delete(url, headers=headers) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert body == rating_delete


async def test_get_ok(session, access_token, likes, access_token_user_2):
    """Проверка получения закладок."""
    _url = f'{settings.fastapi.service_url}{settings.fastapi.RATING_PREFIX}/'
    headers_1 = {'Authorization': 'Bearer ' + access_token}
    headers_2 = {'Authorization': 'Bearer ' + access_token_user_2}
    params_1 = {'rating': settings.data.RATING_1}
    params_2 = {'rating': settings.data.RATING_2}
    url = _url + settings.data.MOVIE_1
    # заполняю фильм оценками
    async with session.post(url, headers=headers_1, params=params_1) as response:
        assert response.status == HTTPStatus.OK
    async with session.post(url, headers=headers_2, params=params_2) as response:
        assert response.status == HTTPStatus.OK
    # Тестирую результат
    async with session.get(url, headers=headers_1) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert body == likes
    # Удаляю тестовые данные
    async with session.delete(url, headers=headers_1) as response:
        assert response.status == HTTPStatus.OK
    async with session.delete(url, headers=headers_2) as response:
        assert response.status == HTTPStatus.OK
