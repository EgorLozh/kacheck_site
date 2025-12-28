# Настройка портов через .env

## Backend

Порт backend сервера настраивается через переменную окружения `BACKEND_PORT` в файле `backend/.env`.

**Пример `backend/.env`:**
```env
BACKEND_PORT=8000
```

Порт используется:
- При запуске через `uvicorn` (нужно указать явно: `--port ${BACKEND_PORT:-8000}`)
- В Docker контейнере через `entrypoint.sh`
- В `docker-compose.yml` для проброса порта

**Для запуска локально:**
```bash
uvicorn src.presentation.main:app --host 0.0.0.0 --port ${BACKEND_PORT:-8000} --reload
```

Или используйте переменную из окружения:
```bash
export BACKEND_PORT=8000
uvicorn src.presentation.main:app --host 0.0.0.0 --port $BACKEND_PORT --reload
```

## Frontend

Порт frontend сервера настраивается через переменную окружения `VITE_PORT` в файле `frontend/.env`.

**Пример `frontend/.env`:**
```env
VITE_PORT=3000
VITE_API_BASE_URL=http://localhost:8000
```

**Важно:** В Vite переменные окружения должны начинаться с префикса `VITE_`, чтобы быть доступными в клиентском коде.

Порт используется:
- В `vite.config.ts` для настройки dev сервера
- `VITE_API_BASE_URL` используется для proxy и прямых API вызовов (если не задан, используется proxy из vite.config.ts)

**Для запуска:**
```bash
npm run dev
```

Сервер автоматически запустится на порту из `VITE_PORT` (по умолчанию 3000).

## Docker

В `docker-compose.yml` порт backend настраивается через переменную `BACKEND_PORT`:

```yaml
ports:
  - "${BACKEND_PORT:-8000}:${BACKEND_PORT:-8000}"
```

Убедитесь, что переменная `BACKEND_PORT` задана в `.env` файле в корне проекта (для docker-compose) или экспортирована в окружении.

## Примеры конфигурации

### Разработка (разные порты)

**`backend/.env`:**
```env
BACKEND_PORT=8000
```

**`frontend/.env`:**
```env
VITE_PORT=3000
VITE_API_BASE_URL=http://localhost:8000
```

### Production (кастомные порты)

**`backend/.env`:**
```env
BACKEND_PORT=5000
```

**`frontend/.env`:**
```env
VITE_PORT=4000
VITE_API_BASE_URL=http://localhost:5000
```


