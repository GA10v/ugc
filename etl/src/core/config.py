from pathlib import Path

from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = Path(Path(__file__).parent.parent.parent, '.env')
        env_file_encoding = 'utf-8'


class ClickhouseSettings(BaseConfig):
    HOST: str = 'localhost'
    PORT: int = 9000
    USER: str = None
    PASSWORD: str = None
    CLUSTER: str = 'company_cluster'
    DATABASE: str = 'default'
    _databases: list[str] = ['shard01', 'shard02', 'shard03']

    TABLES: list[str] = ['views', 'rating']
    FIELDS: dict[str, str] = {
        'user_id': 'String',
        'movie_id': 'String',
        'event': 'UInt64',
        'event_time': 'DateTime DEFAULT now()',
    }

    @property
    def client_conf(self):
        return {
            'host': self.HOST,
            'port': self.PORT,
            'db': self.DATABASE,
            'tables': self.TABLES,
            'fields': self.FIELDS,
            'cluster': self.CLUSTER,
        }

    class Config:
        env_prefix = 'CLICKHOUSE_'


class KafkaSettings(BaseSettings):
    BOOTSTRAP_SERVERS: str = 'localhost:9093'
    CONSUMER_HOST: str = 'localhost:29092'
    TOPICS: list[str] = ['views', 'rating']
    CONSUMER_GROUP: str = 'group-id'
    BATCH_SIZE: int = 10

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


class TransformSettings(BaseConfig):
    batches: dict = {
        'views': [],
        'rating': [],
    }


class ProjectSettings(BaseConfig):
    ch: ClickhouseSettings = ClickhouseSettings()
    kafka: KafkaSettings = KafkaSettings()
    transform: TransformSettings = TransformSettings()


settings = ProjectSettings()
