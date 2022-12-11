from core.config import settings
from .base import BaseOrjsonModel


class Bookmark(BaseOrjsonModel):
	id: str
	user_id: str
	movie_id: str
