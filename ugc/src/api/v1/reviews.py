from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response, Query, Body, Path

from api.v1.utils import ReviewReactionEnum, ReviewSortEnum
from core.config import settings
from models.reviews import ReviewSchema
from services.reviews.client import ReviewService, get_review_service
from utils import auth

router = APIRouter()
auth_handler = auth.AuthHandler()


@router.post(
    path='/',
    response_model=ReviewSchema,
    summary='Добавление рецензии к фильму',
    description='Добавление рецензии к фильму',
)
async def create_review(
    movie_id: str = Query(description="id фильма, которому будет назначена рецензия"),
    text: str = Body(description="Текст рецензии"),
    review_service: ReviewService = Depends(get_review_service),
    _user: dict = Depends(auth_handler.auth_wrapper)
) -> ReviewSchema:
    result = await review_service.create(movie_id=movie_id, text=text, user_id=_user.get('user_id'))
    if not result:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="User can't write more than one movie review")
    return result


@router.put(
    path='/{review_id}/{reaction}',
    response_model=ReviewSchema,
    summary='Добавление лайка или дизлайка к рецензии',
    description='Добавление лайка или дизлайка к рецензии',
)
async def add_review_reaction(
    review_id: str = Path(description="id рецензии, к которой будет добавлен лайк или дизлайк"),
    reaction: ReviewReactionEnum = Path(description="Реакция пользователя"),
    review_service: ReviewService = Depends(get_review_service),
    _user: dict = Depends(auth_handler.auth_wrapper)
) -> ReviewSchema:
    return await review_service.add_like_or_dislike(review_id=review_id, user_id=_user.get('user_id'), reaction=reaction)


@router.get(
    path='/',
    response_model=list[ReviewSchema],
    summary='Просмотр списка рецензий',
    description='Просмотр списка рецензий по фильму с возможностью гибкой сортировки',
)
async def get_reviews(
    movie_id: str = Query(description="id фильма, для которого выводится список рецензий"),
    sort: ReviewSortEnum = Query(description="Параметр сортировки"),
    page_size: Optional[int] = Query(10, gt=0),
    page_number: Optional[int] = Query(1, ge=1),
    review_service: ReviewService = Depends(get_review_service),
    _user: dict = Depends(auth_handler.auth_wrapper)
):
    return await review_service.get_list(movie_id=movie_id, sort=sort, page_size=page_size, page_number=page_number)
