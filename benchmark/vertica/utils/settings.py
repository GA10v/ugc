from pydantic import BaseSettings


class VerticaSettings(BaseSettings):
    HOST: str = 'localhost'
    PORT: int = 5433
    USER = 'dbadmin'
    PASSWORD = ''

    DATABASE: str = 'docker'
    AUTOCOMMIT: bool = True

    @property
    def connection_info(self):
        return {
            'host': self.HOST,
            'port': self.PORT,
            'user': 'dbadmin',
            'password': self.PASSWORD,
            'database': self.DATABASE,
            'autocommit': self.AUTOCOMMIT,
        }


class FieldsSettings(BaseSettings):
    FIELDS: dict[str, str] = {
        'user_id': 'VARCHAR(50) NOT NULL',
        'movie_id': 'VARCHAR(50) NOT NULL',
        'evetn': 'INTEGER NOT NULL',
        'event_time': 'DATETIME NOT NULL',
    }


class TestSettings(BaseSettings):
    TABLE: str = 'benchmark_1'
    UUID: str = '4796fe00-fe9c-4def-a471-a9a4d448b60d'
    BATCHES: list[int] = [1, 10, 100, 1000, 10000]
    STRESS_SIZE: int = 1000000


class BenchmarkSettings(BaseSettings):
    vertica: VerticaSettings = VerticaSettings()
    fields: FieldsSettings = FieldsSettings()
    test_data: TestSettings = TestSettings()


settings = BenchmarkSettings()
