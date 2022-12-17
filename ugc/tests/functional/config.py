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
    RATING_PREFIX: str = '/ugc_api/v1/rating'

    @property
    def service_url(self):
        return f'http://{self.HOST}:{self.PORT}'

    class Config:
        env_prefix = 'TEST_FASTAPI_'


class TestDataSettings(BaseConfig):
    USER: str = '6c162475-c7ed-4461-9184-001ef3d9f264'
    USER_2: str = '8f092fcd-1744-464f-a783-d9a6c4ec59d5'
    MOVIE_1: str = 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a'
    MOVIE_2: str = '26e83050-29ef-4163-a99d-b546cac208f8'
    RATING_1: int = 4
    RATING_2: int = 6


class TestSettings(BaseConfig):
    PROJECT_NAME: str = 'UGC'
    BASE_DIR = Path(__file__).parent.parent
    jwt: JWTSettings = JWTSettings()
    kafka: KafkaSettings = KafkaSettings()
    fastapi: FastapiSettings = FastapiSettings()
    data: TestDataSettings = TestDataSettings()


settings = TestSettings()
