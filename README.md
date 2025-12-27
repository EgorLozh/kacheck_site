# Kacheck - Workout Tracking Application

Приложение для отслеживания тренировок с аналитикой веса, силовых показателей и количества повторений.

## Технологии

**Backend:**
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic (миграции)
- Poetry (управление зависимостями)

**Frontend:**
- React 18 + TypeScript
- React Router
- TanStack Query
- TailwindCSS

## Архитектура

Приложение использует Hexagonal Architecture (Ports & Adapters) с разделением на слои:
- **Domain Layer** - доменные сущности, value objects, доменные сервисы
- **Application Layer** - use cases, DTOs
- **Infrastructure Layer** - реализации репозиториев, база данных, auth
- **Presentation Layer** - FastAPI routers, схемы

## Установка и запуск

### Backend

```bash
cd backend
poetry install
poetry shell
cp env.example .env
```

Настройте переменные окружения в `backend/.env`:
```env
DATABASE_URL=postgresql://user:password@host:port/dbname
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BACKEND_PORT=8000  # Порт для backend сервера
```

Создайте первую миграцию:
```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

Запустите сервер:
```bash
uvicorn src.presentation.main:app --host 0.0.0.0 --port ${BACKEND_PORT:-8000} --reload
```

Или используйте значение из `.env` (после `export BACKEND_PORT=8000` или установки в `.env`):
```bash
uvicorn src.presentation.main:app --host 0.0.0.0 --port $BACKEND_PORT --reload
```

API документация будет доступна по адресу:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Frontend

```bash
cd frontend
npm install
cp env.example .env
# При необходимости отредактируйте .env
npm run dev
```

Переменные окружения в `frontend/.env`:
```env
VITE_PORT=3000  # Порт для frontend сервера (по умолчанию 3000)
VITE_API_BASE_URL=http://localhost:8000  # URL бэкенда (для proxy)
```

Приложение будет доступно по адресу: http://localhost:3000 (или по порту из VITE_PORT)

Для production сборки:
```bash
npm run build
```

### Docker

**Важно:** Если база данных работает на хосте (не в Docker), убедитесь, что `DATABASE_URL` в `.env` использует `host.docker.internal` вместо `127.0.0.1` для Windows/Mac.

См. [DOCKER_DATABASE_SETUP.md](DOCKER_DATABASE_SETUP.md) для подробной информации.

```bash
# Запустить все сервисы (backend + frontend)
docker-compose up --build

# Запустить только backend
docker-compose up backend --build

# Запустить только frontend
docker-compose up frontend --build
```

После запуска:
- Backend: http://localhost:8000 (или порт из BACKEND_PORT)
- Frontend: http://localhost:3000 (или порт из VITE_PORT)

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Регистрация пользователя
- `POST /api/v1/auth/login` - Вход и получение токена

### Exercises
- `GET /api/v1/exercises` - Список упражнений
- `GET /api/v1/exercises/{id}` - Получить упражнение по ID
- `POST /api/v1/exercises` - Создать упражнение (требует аутентификации)
- `PUT /api/v1/exercises/{id}` - Обновить упражнение (требует аутентификации)
- `DELETE /api/v1/exercises/{id}` - Удалить упражнение (требует аутентификации)

### Muscle Groups
- `GET /api/v1/muscle-groups` - Список групп мышц
- `POST /api/v1/muscle-groups` - Создать группу мышц (требует аутентификации)

### Training Templates
- `GET /api/v1/training-templates` - Список шаблонов тренировок
- `POST /api/v1/training-templates` - Создать шаблон (требует аутентификации)

### Trainings
- `GET /api/v1/trainings` - Список тренировок (требует аутентификации)
- `POST /api/v1/trainings` - Создать тренировку (требует аутентификации)

### Analytics
- `GET /api/v1/analytics/weight-progress` - Прогресс веса по упражнению
- `GET /api/v1/analytics/volume-progress` - Прогресс объема по упражнению
- `GET /api/v1/analytics/one-rep-max` - Расчет одноповторного максимума

## Структура проекта

```
kacheck_site/
├── backend/          # FastAPI приложение
│   ├── src/
│   │   ├── domain/      # Domain Layer (entities, value objects, services)
│   │   ├── application/ # Application Layer (use cases, DTOs)
│   │   ├── infrastructure/ # Infrastructure Layer (repositories, DB, auth)
│   │   └── presentation/   # Presentation Layer (FastAPI routers, schemas)
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/         # React приложение (в разработке)
└── docker-compose.yml
```

## Статус проекта

✅ **Backend** - ~90% готов (все основные функции реализованы)
✅ **Frontend** - базовая структура готова (авторизация, layout, базовые страницы)

См. [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) для подробной информации о текущем статусе реализации.

## Быстрый старт

1. **Настройте Backend:**
   ```bash
   cd backend
   poetry install
   poetry shell
   cp env.example .env
   # Отредактируйте .env с вашими настройками БД и BACKEND_PORT
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   uvicorn src.presentation.main:app --host 0.0.0.0 --port ${BACKEND_PORT:-8000} --reload
   ```

2. **Настройте Frontend:**
   ```bash
   cd frontend
   npm install
   cp env.example .env
   # Убедитесь, что VITE_API_BASE_URL указывает на правильный порт backend
   npm run dev
   ```

Подробнее о настройке портов см. [PORTS_CONFIG.md](PORTS_CONFIG.md)

3. Откройте http://localhost:3000 и зарегистрируйтесь/войдите

4. API документация: http://localhost:8000/docs

