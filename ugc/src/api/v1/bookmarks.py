from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from models.bookmarks import BookmarksSchema
from services.bookmarks.client import BookmarkService, get_bookmark_service
from utils import auth

router = APIRouter()
auth_handler = auth.AuthHandler()


@router.post(
    path='/{movie_id}',
    response_model=BookmarksSchema,
    summary='Добавить закладку.',
)
async def add_bookmark(
    movie_id: str,
    bookmark_service: BookmarkService = Depends(get_bookmark_service),
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> BookmarksSchema:
    return await bookmark_service.add(movie_id=movie_id, user_id=_user.get('user_id'))


@router.delete(
    path='/{movie_id}',
    response_model=BookmarksSchema,
    summary='Удалить закладку.',
)
async def delete_bookmark(
    movie_id: str,
    bookmark_service: BookmarkService = Depends(get_bookmark_service),
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> BookmarksSchema:
    _doc = await bookmark_service.delete(movie_id=movie_id, user_id=_user.get('user_id'))
    if not _doc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')
    return _doc


@router.get(
    path='/{user_id}',
    response_model=BookmarksSchema,
    summary='Получить закладки.',
)
async def get_bookmark(
    user_id: str,
    bookmark_service: BookmarkService = Depends(get_bookmark_service),
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> Optional[BookmarksSchema]:
    if user_id == 'me':
        user_id = _user.get('user_id')
    _doc = await bookmark_service.get(user_id=user_id)
    if not _doc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')
    return _doc
