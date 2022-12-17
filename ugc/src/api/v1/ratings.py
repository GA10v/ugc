from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from models.ratings import LikesResponse, RatingSchema, UserRatingSchema
from services.ratings.client import RatingService, get_rating_service
from utils import auth

router = APIRouter()
auth_handler = auth.AuthHandler()


@router.post(
    path='/{movie_id}',
    response_model=RatingSchema,
    summary='Добавить оценку.',
)
async def add_rating(
    movie_id: str,
    rating: int = Query(ge=0, le=10),
    rating_service: RatingService = Depends(get_rating_service),
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> RatingSchema:
    return await rating_service.add(movie_id=movie_id, rating=rating, user_id=_user.get('user_id'))


@router.delete(
    path='/{movie_id}',
    response_model=RatingSchema,
    summary='Удалить оценку.',
)
async def delete_rating(
    movie_id: str,
    rating_service: RatingService = Depends(get_rating_service),
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> RatingSchema:
    return await rating_service.delete(movie_id=movie_id, user_id=_user.get('user_id'))


@router.get(
    path='/{movie_id}',
    response_model=LikesResponse,
    summary='Получить оценку.',
)
async def get_rating(
    movie_id: str,
    rating_service: RatingService = Depends(get_rating_service),
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> Optional[UserRatingSchema]:
    _doc = await rating_service.get(movie_id=movie_id)
    if not _doc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Rating not found')
    return _doc


@router.get(
    path='/{movie_id}/{user_id}',
    response_model=UserRatingSchema,
    summary='Получить оценку.',
)
async def get_user_rating(
    movie_id: str,
    user_id: str,
    rating_service: RatingService = Depends(get_rating_service),
    _user: dict = Depends(auth_handler.auth_wrapper),
) -> Optional[UserRatingSchema]:
    if user_id == 'me':
        user_id = _user.get('user_id')
    _doc = await rating_service.get_one(movie_id=movie_id, user_id=user_id)
    if not _doc:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Rating not found')
    return _doc
