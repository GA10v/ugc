from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Response, Query, Path

from core.config import settings
from models.likes import Like, LikeCount, DislikeCount, LikeAverage
from utils import auth

router = APIRouter()
auth_handler = auth.AuthHandler()


@router.post(
    path='/likes',
    response_model=Like,
    summary='Добавление лайка',
    description='Добавление лайка фильму',
)
def create_like(
    movie_id: str = Query(description='id фильма, которому будет назначен лайк'),
    score: int = Query(ge=0, le=10, description='Оценка лайка по 10-балльной шкале'),
    _user: dict = Depends(auth_handler.auth_wrapper)
):
    pass


@router.delete(
    path='/likes/{like_id}',
    summary='Удаление лайка',
    description='Удаление лайка, адресованного фильму',
)
def delete_like(
    like_id: str = Path(description='id лайка, который будет удален'),
    _user: dict = Depends(auth_handler.auth_wrapper)
):
    pass


@router.put(
    path='/likes/{like_id}',
    response_model=Like,
    summary='Изменение лайка',
    description='Изменение лайка, адресованного фильму',
)
def change_like(
    like_id: str = Path(description='id лайка, оценка которого будет изменена'),
    score: int = Query(ge=0, le=10, description='Новая оценка лайка по 10-балльной шкале'),
    _user: dict = Depends(auth_handler.auth_wrapper)
):
    pass


@router.get(
    path='/likes/count',
    response_model=LikeCount,
    summary='Количество лайков',
    description='Количество лайков, адресованных фильму',
)
def likes_count(
    movie_id: str = Query(description='id фильма, для которого рассчитывается количество лайков'),
    _user: dict = Depends(auth_handler.auth_wrapper)
):
    pass


@router.get(
    path='/dislikes/count',
    response_model=DislikeCount,
    summary='Количество дизлайков',
    description='Количество дизлайков, адресованных фильму',
)
def dislikes_count(
    movie_id: str = Query(description='id фильма, для которого рассчитывается количество дизлайков'),
    _user: dict = Depends(auth_handler.auth_wrapper)
):
    pass


@router.get(
    path='/likes/average',
    response_model=LikeAverage,
    summary='Средняя пользовательская оценка фильма',
    description='Средняя пользовательская оценка фильма',
)
def likes_average(
    movie_id: str = Query(description='id фильма, для которого рассчитывается средняя оценка'),
    _user: dict = Depends(auth_handler.auth_wrapper)
):
    pass
