from typing import Optional, Protocol

from services.ratings.layer_models import Likes, Rating


class RatingRepository(Protocol):
    async def add(self, *args, **kwargs) -> Rating:
        ...

    async def delete(self, *args, **kwargs) -> Rating:
        ...

    async def get(self, *args, **kwargs) -> Optional[Likes]:
        ...
