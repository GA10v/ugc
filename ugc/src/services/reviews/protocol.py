from typing import Optional, Protocol

from services.reviews.layer_models import Review


class ReviewRepository(Protocol):
    async def create(self, movie_id: str, text: str, user_id: str) -> Review:
        ...

    async def add_like_or_dislike(self, review_id: str, user_id: str, reaction: str) -> Review:
        ...

    async def get_list(self, movie_id: str, sort: str, page_size: int, page_number: int) -> list[Review]:
        ...
