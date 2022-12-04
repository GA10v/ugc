from core import settings
from redis import StrictRedis

redis = StrictRedis.from_url(settings.redis.url, decode_responses=True)
