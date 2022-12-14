from pathlib import Path

from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = Path(Path(__file__).parent.parent.parent.parent, '.env')
        env_file_encoding = 'utf-8'


class KafkaSettings(BaseConfig):
    TOPICS: list[str] = ['views', 'rating']

    class Config:
        env_prefix = 'TEST_KAFKA_'


class JWTSettings(BaseConfig):
    SECRET_KEY: str = '245585dbb5cbe2f151742298d61d364880575bff0bdcbf4ae383f0180e7e47dd'
    ALGORITHM: str = 'HS256'

    class Config:
        env_prefix = 'TEST_JWT_'


class FastapiSettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 8000
    EVENT_PREFIX: str = '/ugc_api/v1/event'
    BOOKMARK_PREFIX: str = '/ugc_api/v1/bookmark'

    @property
    def service_url(self):
        return f'http://{self.HOST}:{self.PORT}'

    class Config:
        env_prefix = 'TEST_FASTAPI_'


class MongoSettings(BaseConfig):
    HOST: str = 'mongos1'
    PORT: int = 27019
    DB: str = 'ugc_db'
    BOOKMARK: str = 'test_collection'

    @property
    def uri(self):
        return f'mongodb://{self.HOST}:{self.PORT}'

    class Config:
        env_prefix = 'TEST_MONGO_'


class TestSettings(BaseConfig):
    PROJECT_NAME: str = 'UGC'
    BASE_DIR = Path(__file__).parent.parent
    jwt: JWTSettings = JWTSettings()
    kafka: KafkaSettings = KafkaSettings()
    fastapi: FastapiSettings = FastapiSettings()
    mongo: MongoSettings = MongoSettings()


settings = TestSettings()
