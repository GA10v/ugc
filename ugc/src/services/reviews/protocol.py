from abc import abstractmethod
from typing import Protocol

from services.reviews.layer_models import Review


class ReviewRepository(Protocol):
    @abstractmethod
    async def create(self, movie_id: str, text: str, user_id: str) -> Review:
        ...

    @abstractmethod
    async def add_like_or_dislike(self, review_id: str, user_id: str, reaction: str) -> Review:
        ...

    @abstractmethod
    async def get_list(self, movie_id: str, sort: str, page_size: int, page_number: int) -> list[Review]:
        ...

    @abstractmethod
    async def update(self, movie_id: str, sort: str, page_size: int, page_number: int) -> Review:
        ...

    @abstractmethod
    async def delete(self, movie_id: str, sort: str, page_size: int, page_number: int) -> Review:
        ...
