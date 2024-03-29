from datetime import datetime
from typing import Optional

from api.v1.utils import ReviewReactionEnum, ReviewSortEnum
from bson.objectid import ObjectId
from core.config import settings
from db.mongo import get_mongo
from fastapi import Depends
from models.reviews import ReviewResponse, ReviewSchema
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError
from services.reviews.protocol import ReviewRepository

SORT_CONFIG = {
    ReviewSortEnum.pub_date_asc.value: [{'$sort': {'pub_date': 1}}],
    ReviewSortEnum.pub_date_desc.value: [{'$sort': {'pub_date': -1}}],
    ReviewSortEnum.likes_count_asc.value: [
        {'$addFields': {'count': {'$size': '$likes'}}},
        {'$sort': {'count': 1}},
    ],
    ReviewSortEnum.likes_count_desc.value: [
        {'$addFields': {'count': {'$size': '$likes'}}},
        {'$sort': {'count': -1}},
    ],
    ReviewSortEnum.dislikes_count_asc.value: [
        {'$addFields': {'count': {'$size': '$dislikes'}}},
        {'$sort': {'count': 1}},
    ],
    ReviewSortEnum.dislikes_count_desc.value: [
        {'$addFields': {'count': {'$size': '$dislikes'}}},
        {'$sort': {'count': -1}},
    ],
    ReviewSortEnum.author_score_asc.value: [{'$sort': {'author_score': 1}}],
    ReviewSortEnum.author_score_desc.value: [{'$sort': {'author_score': -1}}],
}


class ReviewService(ReviewRepository):
    def __init__(self, client: AsyncIOMotorClient, collection) -> None:
        self.client = client
        self.collection = collection

    async def _get_author_score(self, movie_id: str, user_id: str) -> Optional[int]:
        """
        Возвращает оценку пользователя.
        :param movie_id: UUID фильма
        :param user_id: UUID пользователя
        :return: int
        """
        _collection = self.client.get_collection(settings.mongo.RATING)
        _doc = await _collection.find_one(
            {'movie_id': movie_id},
            {'_id': 0, 'data': {'$elemMatch': {'user_id': user_id}}},
        )
        if _doc is None:
            return
        try:
            return _doc['data'][0]['rating']
        except KeyError:
            return

    async def _create_doc(self, data: ReviewSchema) -> dict:
        return {
            'movie_id': data['movie_id'],
            'text': data['text'],
            'author_id': data['user_id'],
            'pub_date': data['user_id'],
            'likes': data['likes'],
            'dislikes': data['dislikes'],
            'author_score': await self._get_author_score(data['movie_id'], data['user_id']),
        }

    async def create(self, movie_id: str, text: str, user_id: str) -> ReviewResponse:
        """
        Добавляет рецензию.
        :param movie_id: UUID фильма
        :param text: Текст рецензии
        :param user_id: UUID пользователя
        :return: ReviewSchema
        """
        author_score = await self._get_author_score(movie_id, user_id)
        doc = ReviewSchema(
            movie_id=movie_id,
            text=text,
            author_id=user_id,
        ).dict(exclude={'id'})

        try:
            result = await self.collection.insert_one(doc)
        except DuplicateKeyError:
            return
        _doc = await self.collection.find_one(result.inserted_id)
        response = self._create_doc(_doc)
        return ReviewResponse(id=str(response['_id']), **response)

    async def add_like_or_dislike(self, review_id: str, user_id: str, reaction: ReviewReactionEnum) -> ReviewResponse:
        """
        Добавляет лайк или дизлайк рецензии.
        :param review_id: ID рецензии
        :param user_id: UUID пользователя
        :param reaction: enum лайки или дизлайки
        :return: ReviewSchema
        """
        await self.collection.update_one({'_id': ObjectId(review_id)}, {'$addToSet': {reaction: user_id}})
        response = await self.collection.find_one(ObjectId(review_id))
        return ReviewResponse(id=review_id, **response)

    async def get_list(
        self,
        movie_id: str,
        sort: ReviewSortEnum,
        page_size: int,
        page_number: int,
    ) -> list[ReviewResponse]:
        """
        Возвращает отсортированный список рецензий к фильму.
        :param movie_id: UUID фильма
        :param sort: поле для сортировки
        :param page_size
        :param page_number
        :return: list[ReviewSchema]
        """
        skip_value = page_size * (page_number - 1)
        limit_value = page_size

        agg_list = []
        agg_list.append({'$match': {'movie_id': movie_id}})  # noqa: PIE799
        agg_list.extend(SORT_CONFIG[sort.value])
        agg_list.extend([{'$skip': skip_value}, {'$limit': limit_value}])
        cursor = self.collection.aggregate(agg_list)

        response = []
        for doc in await cursor.to_list(length=None):
            response.append(ReviewResponse(id=str(doc['_id']), **doc))
        return response


async def get_review_service(mongo: AsyncIOMotorClient = Depends(get_mongo)) -> ReviewService:
    collection = mongo.get_collection(settings.mongo.REVIEW)
    await collection.create_index([('author_id', 1), ('movie_id', 1)], unique=True)
    return ReviewService(client=mongo, collection=collection)
