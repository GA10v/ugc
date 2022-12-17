from typing import Optional

from core.config import settings
from db.mongo import get_mongo
from fastapi import Depends
from models.ratings import LikesResponse, RatingSchema, UserRatingSchema
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import WriteError
from services.ratings.protocol import RatingRepository


class RatingService(RatingRepository):
    def __init__(self, client: AsyncIOMotorClient, collection) -> None:
        self.client = client
        self.collection = collection

    async def add(self, movie_id: str, user_id: str, rating: int) -> RatingSchema:
        """
        Добавляет оценку пользователя.
        :param movie_id: UUID фильма
        :param user_id: UUID пользователя
        :param rating: оценка
        :return: RatingSchema
        """
        try:
            await self.collection.update_one(
                {'movie_id': movie_id, 'data.user_id': user_id},
                {'$set': {'data.$.rating': rating}},
                upsert=True,
            )
            # $ - позволяет проходить по спису https://www.mongodb.com/docs/manual/reference/operator/update/positional/
        except WriteError:
            user_rating = {
                'user_id': user_id,
                'rating': rating,
            }
            await self.collection.update_one(
                {'movie_id': movie_id},
                {'$addToSet': {'data': user_rating}},
                upsert=True,
            )

        _response = await self.collection.find_one({'movie_id': movie_id})
        return RatingSchema(**_response)

    async def delete(self, movie_id: str, user_id: str) -> RatingSchema:
        """
        Удаляет оценку пользователя.
        :param movie_id: UUID фильма
        :param user_id: UUID пользователя
        :return: RatingSchema
        """
        await self.collection.update_one(
            {'movie_id': movie_id, 'data.user_id': user_id},
            {'$pull': {'data': {'user_id': user_id}}},
        )
        _response = await self.collection.find_one({'movie_id': movie_id})
        return RatingSchema(**_response)

    async def get(self, movie_id: str) -> Optional[LikesResponse]:
        """
        Возвращает общую оценку.
        :param movie_id: UUID фильма
        :return: LikesResponse
        """
        _doc = await self.collection.find_one({'movie_id': movie_id})
        if _doc is None:
            return

        count_critics = len(_doc.get('data'))
        if count_critics == 0:
            _response = {
                'movie_id': movie_id,
                'likes': [],
                'dislikes': [],
                'rating': 0,
            }
            return LikesResponse(**_response)

        _rating = 0
        likes = []
        dislikes = []
        for user in _doc.get('data'):
            _rating += user.get('rating')
            if user.get('rating') > 5:
                likes.append(user)
                continue
            dislikes.append(user)

        _response = {
            'movie_id': movie_id,
            'likes': likes,
            'dislikes': dislikes,
            'rating': _rating / count_critics,
        }
        return LikesResponse(**_response)

    async def get_one(self, movie_id: str, user_id: str) -> Optional[UserRatingSchema]:
        """
        Возвращает оценку пользователя.
        :param movie_id: UUID фильма
        :param user_id: UUID пользователя
        :return: UserRatingSchema
        """
        _doc = await self.collection.find_one(
            {'movie_id': movie_id},
            {'_id': 0, 'data': {'$elemMatch': {'user_id': user_id}}},
        )
        if _doc is None:
            return
        return UserRatingSchema(**_doc['data'][0])


def get_rating_service(mongo: AsyncIOMotorClient = Depends(get_mongo)) -> RatingService:
    collection = mongo.get_collection(settings.mongo.RATING)
    return RatingService(client=mongo, collection=collection)
