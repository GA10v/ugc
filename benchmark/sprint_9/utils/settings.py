from pydantic import BaseSettings


class ClickHouseSettings(BaseSettings):
    HOST: str = 'localhost'
    USER = 'admin'
    PASSWORD = '123'

    CLUSTER_NAME: str = 'company_cluster'
    DATABASE: str = 'default'
    SHARD_DB: str = 'shard'
    REPLICA_DB: str = 'replica'


class MongoSettings(BaseSettings):
    HOST: str = 'localhost'
    PORT: int = 27017
    DATABASE: str = 'EventDb'
    COLLECTION: str = 'EventCollection'

    @property
    def url(self):
        return f'mongodb://{self.HOST}:{self.PORT}/?directConnection=true'


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


class BenchmarkSettings(BaseSettings):
    clickhouse: ClickHouseSettings = ClickHouseSettings()
    fields: FieldsSettings = FieldsSettings()
    test_data: TestSettings = TestSettings()
    mongo: MongoSettings = MongoSettings()


settings = BenchmarkSettings()
