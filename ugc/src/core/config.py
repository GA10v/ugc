from enum import Enum
from logging import config as logging_config
from pathlib import Path

from core.logger import LOGGING
from pydantic import BaseSettings

logging_config.dictConfig(LOGGING)


class BaseConfig(BaseSettings):
    class Config:
        env_file = Path(Path(__file__).parent.parent.parent.parent, '.env')
        env_file_encoding = 'utf-8'


class MongoSettings(BaseConfig):
    HOST: str = 'mongos1'
    PORT: int = 27019
    DB: str = 'ugc_db'
    BOOKMARK: str = 'bookmark_collection'

    @property
    def uri(self):
        return f'mongodb://{self.HOST}:{self.PORT}'

    class Config:
        env_prefix = 'MONGO_'


class KafkaSettings(BaseConfig):
    BOOTSTRAP_SERVERS: str = 'localhost:9093'
    CONSUMER_HOST: str = 'localhost:29092'
    TOPICS: list[str] = ['views', 'rating']
    CONSUMER_GROUP: str = 'group-id'
    BATCH_SIZE: int = 10

    @property
    def producer_conf(self):
        return {
            'bootstrap_servers': self.BOOTSTRAP_SERVERS,
        }

    @property
    def consumer_conf(self):
        return {
            'host': self.CONSUMER_HOST,
            'topics': self.TOPICS,
            'group_id': self.CONSUMER_GROUP,
            'batch_size': self.BATCH_SIZE,
        }

    class Config:
        env_prefix = 'KAFKA_'


class JWTSettings(BaseConfig):
    SECRET_KEY: str = '245585dbb5cbe2f151742298d61d364880575bff0bdcbf4ae383f0180e7e47dd'
    JWT_TOKEN_LOCATION: list = ['headers']
    ALGORITHM: str = 'HS256'

    class Config:
        env_prefix = 'JWT_'


class FastapiSettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8000
    EVENT_PREFIX: str = '/ugc_api/v1/event'
    BOOKMARK_PREFIX: str = '/ugc_api/v1/bookmark'

    class Config:
        env_prefix = 'FASTAPI_'


class PermissionSettings(Enum):
    User = 0
    Subscriber = 1
    Vip_subscriber = 2
    Moderator = 3


class DebugSettings(BaseConfig):
    DEBUG: bool = True


class ProjectSettings(BaseConfig):
    PROJECT_NAME: str = 'UGC'
    BASE_DIR = Path(__file__).parent.parent
    permission = PermissionSettings
    jwt: JWTSettings = JWTSettings()
    kafka: KafkaSettings = KafkaSettings()
    fastapi: FastapiSettings = FastapiSettings()
    mongo: MongoSettings = MongoSettings()
    debug: DebugSettings = DebugSettings()


settings = ProjectSettings()
