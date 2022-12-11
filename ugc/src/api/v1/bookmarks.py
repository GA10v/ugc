from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Response, Query, Body, Path

from core.config import settings
from models.bookmarks import Bookmark
from utils import auth

router = APIRouter()
auth_handler = auth.AuthHandler()


@router.post(
	path='/bookmarks',
	response_model=Bookmark,
	summary='Добавление фильма в закладки',
	description='Добавление фильма в закладки авторизованного пользователя',
)
def create_bookmark(
	movie_id: str = Query(description="id фильма, который будет добавлен в список закладок"),
	_user: dict = Depends(auth_handler.auth_wrapper)
):
	pass


@router.delete(
	path='/bookmarks/{bookmark_id}',
	summary='Удаление фильма в закладках',
	description='Удаление фильма в закладках авторизованного пользователя',
)
def delete_bookmark(
	bookmark_id: str = Path(description="id закладки, которая будет удалена"),
	_user: dict = Depends(auth_handler.auth_wrapper)
):
	pass


@router.get(
	path='/bookmarks',
	response_model=list[Bookmark],
	summary='Просмотр списка закладок',
	description='Просмотр списка закладок авторизованного пользователя',
)
def get_bookmarks(
	_user: dict = Depends(auth_handler.auth_wrapper)
):
	pass
