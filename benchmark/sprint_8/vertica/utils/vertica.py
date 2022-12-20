import vertica_python
from utils.models import Event
from utils.settings import settings
from vertica_python import connect as _connection


class VerticaClient:
    def __init__(self, dsl: dict) -> None:
        self.dsl = dsl

    def get_conn(self) -> _connection:
        return vertica_python.connect(**self.dsl)

    def create_table(
        self,
        table_name: str,
        fields: dict[str, str] = settings.fields.FIELDS,
    ) -> None:
        """
        Создание таблиц.
        :param table_name: название таблицы
        :param fields: название полей таблицы и их типы
        """

        _fields = ', '.join([f'{key} {value}' for key, value in fields.items()])
        command = f'CREATE TABLE IF NOT EXISTS {table_name} ({_fields});'
        with self.get_conn() as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(command)
            except Exception as ex:
                raise ex

    def insert(self, table_name: str, data: list[Event]) -> None:
        """
        Вставка данных в таблицу
        :param table_name: название таблицы
        :param data: сипсок событий
        """

        _fields = ', '.join(Event._fields)
        _placeholders = ', '.join(['%s'] * len(Event._fields))
        with self.get_conn() as connection:
            cursor = connection.cursor()
            try:
                cursor.executemany(f'INSERT INTO {table_name} ({_fields}) VALUES ({_placeholders})', data)
            except Exception as ex:
                raise ex

    def select(self, table_name: str, fields: list[str] = None, movie_id: str = None) -> list:
        """
        Получение данных из таблицы.
        :param table_name: название таблицы
        :param data: сипсок событий
        param movie_id: UUID
        """

        if fields:
            fields = ', '.join(fields)
        else:
            fields = '*'
        command = f'SELECT {fields} FROM {table_name}'

        if movie_id:
            command += f" WHERE movie_id = '{movie_id}'"

        with self.get_conn() as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(command)
            except Exception as ex:
                raise ex
