# Тест хранилища ClickHouse

## Запуск теста
1. Запустить контейнер командой  ```$ docker-compose up -d```
2. Последовательно выполнить скрипты в файле ```test_ch.ipynb```

## Результаты теста

### Tecт 1: Тестирование вставки данных о событиях с разным размером батча. (нет записей в таблице)

========================================
- Batch size: 1 items;
Загрузка батчами выполнена за 0.01766
========================================
- Batch size: 10 items;
Загрузка батчами выполнена за 0.01685
========================================
- Batch size: 100 items;
Загрузка батчами выполнена за 0.02217
========================================
- Batch size: 1000 items;
Загрузка батчами выполнена за 0.22511
========================================
- Batch size: 10000 items;
Загрузка батчами выполнена за 0.74639

### Tecт 2: Тестирование поиска данных о событиях. (< 15_000 записей в таблице)

========================================
- Records: 11211 items;
- Поиск фильма выполнена за 0.06883

### Tecт 3: Тестирование вставки батча в 1_000_000 записей. (< 15_000 записей в таблице).

========================================
- Batch size: 1000000 items;
Загрузка батчами выполнена за 62.8587

### Tecт 4: Тестирование вставки данных о событиях с разным размером батча. (1_000_000 записей в таблице).

========================================
- Batch size: 1 items;
Загрузка батчами выполнена за 0.01103
========================================
- Batch size: 10 items;
Загрузка батчами выполнена за 0.00833
========================================
- Batch size: 100 items;
Загрузка батчами выполнена за 0.01505
========================================
- Batch size: 1000 items;
Загрузка батчами выполнена за 0.11646
========================================
- Batch size: 10000 items;
Загрузка батчами выполнена за 0.75701

### Тест 5: Тестирование поиска данных о событиях. (1_000_000 записей в таблице)

========================================
- Records: 1022422 items;
Поиск фильма выполнена за 0.55199

### Тест 6: Тестирование обновления данных о событиях. (1_000_000 записей в таблице)

========================================
- Records: 1022522 items;
Тест обновления выполнен за 0.16358