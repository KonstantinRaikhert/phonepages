[![codestyle PEP8](https://github.com/raikhert13/phonepages/actions/workflows/codestyle.yaml/badge.svg)](https://github.com/raikhert13/phonepages/actions/workflows/codestyle.yaml)
# Телефонный справочник компаний (тестовое задание)
Справочник представляет собой API приложение(DFR) для поиска номеров телефонов и информации об организациях.
## Возможности:
 - аутентификация по почте и паролю(DRF token)
 - API компаний
 - API сотрудников компаний
 - API поиска по сотрудникам, названию фирмы, номерам телефонов
## Технологии:
```
Python 3.8
Django 3.2
Django REST Framework 3.12
Django Filters
Postgres SQL
Factory Boy
Poetry
Docker
pre-commit hooks
```
## Структура проекта
```
├── README.md
├── infra
├── project-settings
├── requirements
├── users
└── corporations
```
1. В папке **infra** находятся docker-compose скрипты:
- для локального запуска Postgres выполните:
```
docker-compose -f local.yaml up --build
```
- для запуска всего приложения:
```
docker-compose -f develop.yaml up --build
```
Так же в папке **infra** находятся примеры файлов переменных окружения:
- для Django - **.django**
```
DJANGO_SECRET_KEY=secret.key
DJANGO_ALLOWED_HOSTS=localhost,0.0.0.0,127.0.0.1
DJANGO_SUPERUSER_EMAIL=admin@admin.ru
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_FIRSTNAME=admin
DJANGO_SUPERUSER_LASTNAME=admin
DJANGO_SUPERUSER_PASSWORD=admin
```
- для Postgres - **.postgres**
```
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=phonebook_dev
POSTGRES_USER=user
POSTGRES_PASSWORD=password
```
- для Postgres(локально) - **.postgres_local**
2. В **project-settings** находятся настройки Django и DRF
3. **users** и **corporations** приложения Django
4. В **requirements** - зависимости проекта

По желанию можно использовать Poetry(менеджер зависимостей):
```
poetry shell
poetry install
```
и pre-commit hooks:
```
pre-commit install --all
```
## Заполнение БД тестовыми данными
В проекте есть 2 кастомные команды:
1. Создаёт суперпользователя с данными из переменных окружения
```
python manage.py createadmin
```
2. Команда, использующая библиотеку **Factory boy**, заполняет пользователями, профессиями, телефонами, фирмами
```
python manage.py filldb
```
используйте аргумент **-help** для дополнительной информации
## Документация API
Доступны по адресам:

[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

[http://127.0.0.1:8000/swagger](http://127.0.0.1:8000/swagger)

### Недоделки:
Возможно их немало. Но в первую очередь -  некоторые валидаторы и автодокументация
