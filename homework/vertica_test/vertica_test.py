import vertica_python

connection_info = {
    'host': '127.0.0.1',
    'port': 5433,
    'user': 'dbadmin',
    'password': '',
    'database': 'docker',
    'autocommit': True,
} 

# создать таблицу для сохранения прогресса просмотра фильмов
with vertica_python.connect(**connection_info) as connection:
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE views (
        id IDENTITY,
        user_id INTEGER NOT NULL,
        movie_id VARCHAR(256) NOT NULL,
        viewed_frame INTEGER NOT NULL
    );
    """)

# записать данные о просмотре во вновь созданную таблицу
with vertica_python.connect(**connection_info) as connection:
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO views (user_id, movie_id, viewed_frame) VALUES (
    5002711,
    'tt01203381',
    1611902872
); 
    """)

# посчитать данные
with vertica_python.connect(**connection_info) as connection:
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * FROM views;
    """)
    for row in cursor.iterate():
        print(row)