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
    PORT: int = 27017
    DB: str = 'ugc_db'

    class Config:
        env_prefix = 'MONGO_'


class JWTSettings(BaseConfig):
    SECRET_KEY: str = '245585dbb5cbe2f151742298d61d364880575bff0bdcbf4ae383f0180e7e47dd'
    JWT_TOKEN_LOCATION: list = ['headers']
    ALGORITHM: str = 'HS256'

    class Config:
        env_prefix = 'JWT_'


class FastapiSettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8002
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


class ProjectSettings(BaseConfig):
    PROJECT_NAME: str = 'UGC_2'
    BASE_DIR = Path(__file__).parent.parent
    permission = PermissionSettings
    jwt: JWTSettings = JWTSettings()
    mongo: MongoSettings = MongoSettings()
    fastapi: FastapiSettings = FastapiSettings()
    debug: DebugSettings = DebugSettings()


settings = ProjectSettings()
