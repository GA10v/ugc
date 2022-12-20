import uuid
from http import HTTPStatus

import jwt
import pytest
from config import settings

pytestmark = pytest.mark.asyncio


@pytest.fixture
def review_user_ids():
    return [settings.data.USER, settings.data.USER_2, settings.data.USER_3]


@pytest.fixture
def review_movie_id():
    return settings.data.MOVIE_1


@pytest.fixture
def review_text():
    return 'Review text'


@pytest.fixture
def review_access_tokens(review_user_ids):
    result = []
    for user_id in review_user_ids:
        data = {'sub': user_id, 'permissions': [], 'is_super': True}
        result.append(jwt.encode(data, settings.jwt.SECRET_KEY, settings.jwt.ALGORITHM))
    return result


async def test_get_unauthorized(session):
    """Проверка доступа неавторизованного пользователя."""
    url = f'{settings.fastapi.service_url}{settings.fastapi.REVIEW_PREFIX}/'
    async with session.get(url) as response:
        assert response.status == HTTPStatus.FORBIDDEN


async def test_create(session, review_user_ids, review_movie_id, review_text, review_access_tokens):
    """Проверка добавления рецензии."""
    user_index = 0

    url = f'{settings.fastapi.service_url}{settings.fastapi.REVIEW_PREFIX}/'
    headers = {'Authorization': 'Bearer ' + review_access_tokens[user_index]}
    params = {'movie_id': review_movie_id}
    data = review_text

    async with session.post(url, headers=headers, params=params, data=data) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert body['movie_id'] == review_movie_id
        assert body['text'] == review_text
        assert body['author_id'] == review_user_ids[user_index]

    async with session.post(url, headers=headers, params=params, data=data) as response:
        assert response.status == HTTPStatus.CONFLICT


async def test_add_like(session, review_user_ids, review_movie_id, review_text, review_access_tokens):
    """Проверка добавления лайка к рецензии."""
    user_index = 1

    url_1 = f'{settings.fastapi.service_url}{settings.fastapi.REVIEW_PREFIX}/'
    headers = {'Authorization': 'Bearer ' + review_access_tokens[user_index]}
    params = {'movie_id': review_movie_id}
    data = review_text
    async with session.post(url_1, headers=headers, params=params, data=data) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        review_id = body['id']

    url_2 = f'{settings.fastapi.service_url}{settings.fastapi.REVIEW_PREFIX}/{review_id}/likes'
    async with session.put(url_2, headers=headers) as response:
        assert response.status == HTTPStatus.OK

    params = {'movie_id': review_movie_id, 'sort': 'pub_date_desc'}
    async with session.get(url_1, headers=headers, params=params) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert len(body[0]['likes']) == 1

    async with session.put(url_2, headers=headers) as response:
        assert response.status == HTTPStatus.OK

    async with session.get(url_1, headers=headers, params=params) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert len(body[0]['likes']) == 1


async def test_add_dislike(session, review_user_ids, review_movie_id, review_text, review_access_tokens):
    """Проверка добавления дизлайка к рецензии."""
    user_index = 2

    url_1 = f'{settings.fastapi.service_url}{settings.fastapi.REVIEW_PREFIX}/'
    headers = {'Authorization': 'Bearer ' + review_access_tokens[user_index]}
    params = {'movie_id': review_movie_id}
    data = review_text
    async with session.post(url_1, headers=headers, params=params, data=data) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        review_id = body['id']

    url_2 = f'{settings.fastapi.service_url}{settings.fastapi.REVIEW_PREFIX}/{review_id}/dislikes'
    async with session.put(url_2, headers=headers) as response:
        assert response.status == HTTPStatus.OK

    params = {'movie_id': review_movie_id, 'sort': 'pub_date_desc'}
    async with session.get(url_1, headers=headers, params=params) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert len(body[0]['dislikes']) == 1

    async with session.put(url_2, headers=headers) as response:
        assert response.status == HTTPStatus.OK

    async with session.get(url_1, headers=headers, params=params) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert len(body[0]['dislikes']) == 1


async def test_get_list(session, review_user_ids, review_movie_id, review_text, review_access_tokens):
    """Вывод списка рецензий к фильму с пагинацией и сортировкой"""
    user_index = 0

    url = f'{settings.fastapi.service_url}{settings.fastapi.REVIEW_PREFIX}/'
    headers = {'Authorization': 'Bearer ' + review_access_tokens[user_index]}
    params = {'movie_id': review_movie_id, 'sort': 'pub_date_desc'}
    async with session.get(url, headers=headers, params=params) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert len(body) == 3

    params['page_size'] = 2
    async with session.get(url, headers=headers, params=params) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert len(body) == 2
        assert body[0]['author_id'] == review_user_ids[2]
        assert body[1]['author_id'] == review_user_ids[1]

    params['page_number'] = 2
    async with session.get(url, headers=headers, params=params) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert len(body) == 1
        assert body[0]['author_id'] == review_user_ids[0]

