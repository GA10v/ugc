from enum import Enum
# from logging import config as logging_config
from pathlib import Path

# from core.logger import LOGGING
from pydantic import BaseSettings

# logging_config.dictConfig(LOGGING)


class BaseConfig(BaseSettings):
    class Config:
        env_file = Path(Path(__file__).parent.parent.parent.parent, '../../../.env')
        env_file_encoding = 'utf-8'


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
    PREFIX: str = '/ugc_api/v1/event'

    class Config:
        env_prefix = 'FASTAPI_'


class PermissionSettings(Enum):
    User = 0
    Subscriber = 1
    Vip_subscriber = 2
    Moderator = 3


class DebugSettings(BaseConfig):
    DEBUG: bool = True


class LogingSettings(BaseConfig):
    SENTRY_DSN: str = ''
    LOGSTAH_HOST: str = 'logstash'
    LOGSTAH_PORT: int = 5044

    class Config:
        env_prefix = 'LOGGING_'


class ProjectSettings(BaseConfig):
    PROJECT_NAME: str = 'UGC'
    BASE_DIR = Path(__file__).parent.parent
    permission = PermissionSettings
    jwt: JWTSettings = JWTSettings()
    kafka: KafkaSettings = KafkaSettings()
    fastapi: FastapiSettings = FastapiSettings()
    debug: DebugSettings = DebugSettings()
    logging: LogingSettings = LogingSettings()


settings = ProjectSettings()
