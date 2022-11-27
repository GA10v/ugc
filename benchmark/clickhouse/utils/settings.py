from pydantic import BaseSettings


class ClickHouseSettings(BaseSettings):
    HOST: str = 'localhost'
    USER = 'admin'
    PASSWORD = '123'

    CLUSTER_NAME: str = 'company_cluster'
    DATABASE: str = 'ch_benchmark'
    SHARD_DB: str = 'shard'
    REPLICA_DB: str = 'replica'


class FieldsSettings(BaseSettings):
    FIELDS: dict[str, str] = {
        'user_id': 'String',
        'movie_id': 'String',
        'evetn': 'UInt64',
        'event_time': 'DateTime DEFAULT now()',
    }
    PARTITION: str = None
    ORDER: str = 'movie_id'


class BenchmarkSettings(BaseSettings):
    clickhouse: ClickHouseSettings = ClickHouseSettings()
    fields: FieldsSettings = FieldsSettings()


settings = BenchmarkSettings()
