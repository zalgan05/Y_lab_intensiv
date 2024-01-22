# Y_lab домашнее задание

Задача: написать проект на FastAPI с использованием PostgreSQL в качестве БД. В проекте следует реализовать REST API по работе с меню ресторана, все CRUD операции/

## Запуска проекта

1. Склонировать репозиторий
```py
git@github.com:zalgan05/Y_lab_intensiv.git
```
3. Создать сервер БД PostgreSQL
4. Создать файл .env и заполнить его своими данными. Пример:
```py
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASS=postgres
```
4. Создать виртуальное окружение и установить зависимости
```py
python -m venv venv
source venv\Scripts\activate
pip install -r requirements.txt
```
5. Применить миграции
```py
alembic upgrade head
```
6. Запустить сервер
```py
python main.py
```

## Стек технологий
* Alembic
* FastAPI
* SQLAlchemy
* PostgeSQL
