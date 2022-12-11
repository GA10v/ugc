import json
from functools import lru_cache
from os import getenv

from pydantic import BaseConfig


class TestConfig(BaseConfig):
    FASTAPI_HOST: str = getenv("FASTAPI_HOST")
    FASTAPI_PORT: str = getenv("FASTAPI_PORT")
    FASTAPI_PREFIX: str = getenv("FASTAPI_PREFIX")
    JWT_SECRET_KEY: str = getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = getenv("JWT_ALGORITHM")
    KAFKA_TOPICS: list[str] = json.loads(getenv("KAFKA_TOPICS"))

    @property
    def service_url(self):
        return f"http://{self.FASTAPI_HOST}:{self.FASTAPI_PORT}"

    @property
    def service_prefix(self):
        return self.FASTAPI_PREFIX

    class Config:
        frozen = True


@lru_cache()
def get_config() -> TestConfig:
    return TestConfig()
