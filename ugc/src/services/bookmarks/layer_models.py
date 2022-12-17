from pydantic import BaseModel


class Bookmarks(BaseModel):
    user_id: str
    bookmarks: list[str]
