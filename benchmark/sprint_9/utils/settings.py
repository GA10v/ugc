from pydantic import BaseSettings


class ClickHouseSettings(BaseSettings):
    HOST: str = 'localhost'
    USER = 'admin'
    PASSWORD = '123'

    CLUSTER_NAME: str = 'company_cluster'
    DATABASE: str = 'default'
    SHARD_DB: str = 'shard'
    REPLICA_DB: str = 'replica'


class FieldsSettings(BaseSettings):
    FIELDS: dict[str, str] = {
        'user_id': 'String',
        'movie_id': 'String',
        'rating': 'UInt64',
        'event_time': 'DateTime DEFAULT now()',
    }
    PARTITION: str = None
    ORDER: str = 'movie_id'


class TestSettings(BaseSettings):
    TABLE: str = 'reviews'
    UUID: str = '4796fe00-fe9c-4def-a471-a9a4d448b60d'
    BATCHES: list[int] = [1, 10, 100, 1000, 10000]
    STRESS_SIZE: int = 1000000


class BenchmarkSettings(BaseSettings):
    clickhouse: ClickHouseSettings = ClickHouseSettings()
    fields: FieldsSettings = FieldsSettings()
    test_data: TestSettings = TestSettings()


settings = BenchmarkSettings()
