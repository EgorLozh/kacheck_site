# Kacheck Backend

Backend приложение для отслеживания тренировок.

## Установка

1. Установите Poetry (если еще не установлен):
```bash
pip install poetry
```

2. Установите зависимости:
```bash
poetry install
```

3. Активируйте виртуальное окружение:
```bash
poetry shell
```

4. Создайте файл `.env` на основе `env.example`:
```bash
cp env.example .env
```

5. Настройте переменные окружения в `.env`:
- `DATABASE_URL` - строка подключения к PostgreSQL
- `SECRET_KEY` - секретный ключ для JWT
- `BACKEND_PORT` - порт для backend сервера (по умолчанию 8000)
- Остальные настройки опциональны

6. Запустите миграции:
```bash
alembic upgrade head
```

7. Запустите сервер:
```bash
uvicorn src.presentation.main:app --host 0.0.0.0 --port ${BACKEND_PORT:-8000} --reload
```

Или используйте значение из settings (требует изменения для использования переменной окружения):
```bash
uvicorn src.presentation.main:app --host 0.0.0.0 --port 8000 --reload
```

## Структура проекта

Проект следует Hexagonal Architecture (DDD):

- `src/domain/` - Доменный слой (entities, value objects, services, repository interfaces)
- `src/application/` - Слой приложения (use cases, DTOs)
- `src/infrastructure/` - Инфраструктурный слой (реализации репозиториев, БД, auth)
- `src/presentation/` - Слой представления (FastAPI routers, schemas)

## Развертывание через Docker

```bash
docker-compose up --build
```

