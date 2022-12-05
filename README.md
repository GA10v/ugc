# Проектная работа 8 спринта

Ссылка на [проект](https://github.com/GA10v/ugc_sprint_1)

## Работа с проектом

Для работы с сервисом UGC необходимо получить access_token в сервисе [Auth](https://github.com/GA10v/Auth_sprint_2)

### Запуск приложения UGC локально
1. Установить зависимости командой
    ```$ poetry install```
2. Создать файл конфигурации ```.env``` в корне проекта и заполнить его согласно ```example.env ```
3. Cервис ETL запускается командой
    ```$ python3 etl/src/main.py```
4. Сервис UGC запускается командой
    ```$ python3 ugc/src/main.py```
5. Перейти к документации по url: ```http://localhost:8001/api/openapi```


### Запуск приложения в docker
1. Создать файл конфигурации ```.env``` в корне проекта и заполнить его согласно ```example.env ```
2. Запустить контейнер командой
    ```$ docker-compose -f docker-compose.prod.yml up -d --build ```
3. Перейти к документации по url: ```http://localhost:8001/api/openapi```
