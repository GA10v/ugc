from abc import abstractmethod
from typing import Optional, Protocol

from services.bookmarks.layer_models import Bookmarks


class BookmarkRepository(Protocol):
    @abstractmethod
    async def add(self, *args, **kwargs) -> Bookmarks:
        ...

    @abstractmethod
    async def delete(self, *args, **kwargs) -> Bookmarks:
        ...

    @abstractmethod
    async def get(self, *args, **kwargs) -> Optional[Bookmarks]:
        ...
