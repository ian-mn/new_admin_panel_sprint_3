# Проектное задание: ETL
![Black](https://img.shields.io/badge/code%20style-black-black)
[![Maintainability](https://api.codeclimate.com/v1/badges/2a3910f5a464aba50670/maintainability)](https://codeclimate.com/github/ian-mn/new_admin_panel_sprint_3/maintainability)

## Задание спринта

Написать отказоустойчивый перенос данных из Postgres в Elasticsearch

## Требования

- Используйте предложенную [cхему индекса](https://code.s3.yandex.net/middle-python/learning-materials/es_schema.txt)💾  `movies`, в которую должна производиться загрузка фильмов. В конце этого урока вы найдёте пояснения к ней.
- Ваш код должен корректно вести себя при потере связи с ES или Postgres. Используйте технику backoff, чтобы ваш сервис не мешал восстановлению БД.
- При перезапуске приложения оно должно продолжить работу с места остановки, а не начинать процесс заново. Здесь вам поможет хранение состояния.
- ES с загруженными данными успешно проходит [Postman-тесты](https://code.s3.yandex.net/middle-python/learning-materials/ETLTests-2.json)💾. Подробнее об этом способе тестирования мы расскажем в следующем уроке.

## Комментарии по работе
- При запуске данные переносятся из SQLite в PostgreSQL;
- Extract, Transform и Load обрабатывают данные пачками;
- Записи из БД валидируются с помощью pydantic;
- Extract происходит с последней обработанной записи;
- ETL срабатывает при закуске docker-compose, далее раз в минуту вычитывает изменившиеся записи при помощи APScheduler;
- За хранение последней обработанной записи отвечает State;
- Там же хранится состояние начала/окончания записи, чтобы несколько процессов ETL не накладывались друг на друга;
- State использует как хранилище либо Redis, либо JSON-файл;
- При потере соединения с PostgreSQL, Redis или ElasticSearch процесс ждет, пока сервисы восстановятся с помощью exponential backoff;
- Тесты Postman перенесены в `docker-compose.tests.yml`, где их выполняет Newman.


