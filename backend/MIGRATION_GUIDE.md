# Руководство по миграциям Alembic

## Создание первой миграции

1. Убедитесь, что файл `.env` настроен с правильным `DATABASE_URL`

2. Создайте первую миграцию:
```bash
cd backend
alembic revision --autogenerate -m "Initial migration"
```

3. Проверьте созданный файл миграции в `src/infrastructure/migrations/versions/`

4. Примените миграцию:
```bash
alembic upgrade head
```

## Создание новых миграций

После изменения моделей SQLAlchemy:

```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

## Откат миграций

```bash
# Откатить одну миграцию
alembic downgrade -1

# Откатить все миграции
alembic downgrade base
```

## Проверка текущей версии

```bash
alembic current
```

## История миграций

```bash
alembic history
```





