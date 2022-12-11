from datetime import date

from pydantic import Field

from core.config import settings
from .base import BaseOrjsonModel


class MetaInfo(BaseOrjsonModel):
	author_id: str
	pub_date: date

	def dict(self, *args, **kwargs) -> dict:
		_dict: dict = super().dict(*args, **kwargs)
		_dict['pub_date'] = _dict['pub_date'].strftime('%Y-%m-%d')
		return _dict


class RelatedData(BaseOrjsonModel):
	likes: list[str] = Field(default_factory=list)
	dislikes: list[str] = Field(default_factory=list)
	author_score: int = None


class Review(BaseOrjsonModel):
	id: str
	text: str
	additional_info: MetaInfo
	related_data: RelatedData

