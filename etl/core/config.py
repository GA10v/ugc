from pathlib import Path

from pydantic import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = Path(Path(__file__).parent.parent.parent, '.env')
        env_file_encoding = 'utf-8'


class ClickhouseSettings(BaseConfig):
    HOST: str = 'localhost'
    MASTER_PORT: int = 9000
    SUB_PORTS: list[int] = [9001, 9002]
    USER: str = None
    PASSWORD: str = None
    CLUSTER: str = 'company_cluster'
    DATABASE: str = 'default'
    databases: list[str] = ['shard01', 'shard02', 'shard03']

    TABLES: list[str] = ['views', 'rating']
    FIELDS: dict[str, str] = {
        'user_id': 'String',
        'movie_id': 'String',
        'evetn': 'UInt64',
        'event_time': 'DateTime DEFAULT now()',
    }

    @property
    def client_conf(self):
        return {
            'host': self.HOST,
            'port': self.MASTER_PORT,
            'sub': self.SUB_PORTS,
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


class ProjectSettings(BaseConfig):
    ch: ClickhouseSettings = ClickhouseSettings()
    kafka: KafkaSettings = KafkaSettings()


settings = ProjectSettings()
