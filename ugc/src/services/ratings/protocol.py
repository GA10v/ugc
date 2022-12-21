from abc import abstractmethod
from typing import Optional, Protocol

from services.ratings.layer_models import Likes, Rating, UserRating


class RatingRepository(Protocol):
    @abstractmethod
    async def add(self, *args, **kwargs) -> Rating:
        ...

    @abstractmethod
    async def delete(self, *args, **kwargs) -> Rating:
        ...

    @abstractmethod
    async def get(self, *args, **kwargs) -> Optional[Likes]:
        ...

    @abstractmethod
    async def get_one(self, *args, **kwargs) -> Optional[UserRating]:
        ...
