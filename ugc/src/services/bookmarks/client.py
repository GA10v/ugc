from typing import Optional

from core.config import settings
from db.mongo import get_mongo
from fastapi import Depends
from models.bookmarks import BookmarksSchema
from motor.motor_asyncio import AsyncIOMotorClient
from services.bookmarks.protocol import BookmarkRepository


class BookmarkService(BookmarkRepository):
    def __init__(self, client: AsyncIOMotorClient, collection) -> None:
        self.client = client
        self.collection = collection

    async def add(self, movie_id: str, user_id: str) -> BookmarksSchema:
        """
        Добавляет закладку.
        :param movie_id: UUID фильма
        :param user_id: UUID пользователя
        :return: BookmarksSchema
        """
        await self.collection.update_one({'user_id': user_id}, {'$addToSet': {'bookmarks': movie_id}}, upsert=True)
        # $addToSet - добавляет уникальный элемент в массив https://www.mongodb.com/docs/manual/reference/operator/update/addToSet/ # noqa: E501
        # upsert - выполнит вставку если не найдет совпадений по фильтру https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html#motor.motor_asyncio.AsyncIOMotorCollection.update_one # noqa: E501
        _response = await self.collection.find_one({'user_id': user_id})
        return BookmarksSchema(**_response)

    async def delete(self, movie_id: str, user_id: str) -> BookmarksSchema:
        """
        Удаляет закладку.
        :param movie_id: UUID фильма
        :param user_id: UUID пользователя
        :return: BookmarksSchema
        """
        await self.collection.update_one({'user_id': user_id}, {'$pull': {'bookmarks': movie_id}})
        _response = await self.collection.find_one({'user_id': user_id})
        return BookmarksSchema(**_response)

    async def get(self, user_id: str) -> Optional[BookmarksSchema]:
        """
        Возвращает документ.
        :param user_id: UUID пользователя
        :return: BookmarksSchema | None
        """
        _response = await self.collection.find_one({'user_id': user_id})
        if _response is None:
            return
        return BookmarksSchema(**_response)


def get_bookmark_service(mongo: AsyncIOMotorClient = Depends(get_mongo)) -> BookmarkService:
    collection = mongo.get_collection(settings.mongo.BOOKMARK)
    return BookmarkService(client=mongo, collection=collection)
