from core.config import settings
from .base import BaseOrjsonModel


class Like(BaseOrjsonModel):
	id: str
	user_id: str
	movie_id: str
	score: int


class LikeCount(BaseOrjsonModel):
	movie_id: str
	total_likes_count: int


class DislikeCount(BaseOrjsonModel):
	movie_id: str
	total_dislikes_count: int


class LikeAverage(BaseOrjsonModel):
	movie_id: str
	average_score: int
