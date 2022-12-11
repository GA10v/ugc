from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Response, Query, Body, Path

from core.config import settings
from models.reviews import Review
from utils import auth

router = APIRouter()
auth_handler = auth.AuthHandler()


@router.post(
    path='/reviews',
    response_model=Review,
    summary='Добавление рецензии к фильму',
    description='Добавление рецензии к фильму',
)
def create_review(
    movie_id: str = Query(description="id фильма, которому будет назначена рецензия"),
    text: str = Body(description="Текст рецензии"),
    _user: dict = Depends(auth_handler.auth_wrapper)
):
    pass


@router.put(
    path='/reviews/{review_id}/likes',
    response_model=Review,
    summary='Добавление лайка к рецензии',
    description='Добавление лайка к рецензии',
)
def add_review_like(
    review_id: str = Path(description="id рецензии, к которой будет добавлен лайк"),
    _user: dict = Depends(auth_handler.auth_wrapper)
):
    pass


@router.put(
    path='/reviews/{review_id}/dislikes',
    response_model=Review,
    summary='Добавление дизлайка к рецензии',
    description='Добавление дизлайка к рецензии',
)
def add_review_dislike(
    review_id: str = Path(description="id рецензии, к которой будет добавлен дизлайк"),
    _user: dict = Depends(auth_handler.auth_wrapper)
):
    pass


@router.get(
    path='/reviews',
    response_model=list[Review],
    summary='Просмотр списка рецензий',
    description='Просмотр списка рецензий по фильму с возможностью гибкой сортировки',
)
def get_reviews(
    movie_id: str = Query(description="id фильма, для которого выводится список рецензий"),
    sort: str = Query(description="Параметр сортировки"),
    _user: dict = Depends(auth_handler.auth_wrapper)
):
    pass
