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
    CLUSTER: str = 'company_cluster'
    DATABASE: str = 'default'

    TABLES: list[str] = ['ugc_event']
    FIELDS: dict[str, str] = {
        'user_id': 'VARCHAR(50) NOT NULL',
        'movie_id': 'VARCHAR(50) NOT NULL',
        'evetn': 'INTEGER NOT NULL',
        'event_time': 'DATETIME NOT NULL',
    }

    class Config:
        env_prefix = 'CLICKHOUSE_'


class ProjectSettings(BaseConfig):
    ch: ClickhouseSettings = ClickhouseSettings()


settings = ProjectSettings()
