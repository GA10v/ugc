from typing import Protocol

from services.bookmarks.layer_models import Bookmarks


class NotFoundError(Exception):
    ...


class BookmarkRepository(Protocol):
    async def add(self, *args, **kwargs) -> Bookmarks:
        ...

    async def delete(self, *args, **kwargs) -> Bookmarks:
        ...

    async def get(self, *args, **kwargs) -> Bookmarks:
        """
        :raises NotFoundError:
        """
        ...
