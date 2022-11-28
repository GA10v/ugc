from pathlib import Path

from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = Path(Path(__file__).parent.parent.parent, '.env')
        env_file_encoding = 'utf-8'


class ClickhouseSettings(BaseConfig):
    URL: str = 'http://localhost:8123/'
    USER: str = None
    PASSWORD: str = None
    DATABASE: str = 'default'
    TABLE: str = 'ugc'

    class Config:
        env_prefix = 'CLICKHOUSE_'


class ProjectSettings(BaseConfig):
    ch: ClickhouseSettings = ClickhouseSettings()


settings = ProjectSettings()
