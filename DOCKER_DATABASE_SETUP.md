# Настройка подключения к внешней БД из Docker

## Проблема

Docker контейнер не может подключиться к базе данных на хосте, используя `127.0.0.1` или `localhost`.

## Решение

### Вариант 1: Использование host.docker.internal (Windows/Mac)

В `docker-compose.yml` добавлен `extra_hosts` для доступа к хосту.

В файле `.env` (в корне проекта, для docker-compose) измените `DATABASE_URL`:

**Для Windows/Mac:**
```env
DATABASE_URL=postgresql://postgres:password@host.docker.internal:5432/kacheck_bot
```

**Важно:** Замените `127.0.0.1` на `host.docker.internal` в DATABASE_URL.

### Вариант 2: Использование IP адреса хоста

Если `host.docker.internal` не работает, используйте реальный IP адрес вашего хоста:

1. Найдите IP адрес вашего хоста:
   ```bash
   # Windows
   ipconfig
   
   # Linux/Mac
   ifconfig
   ```

2. Используйте этот IP в DATABASE_URL:
   ```env
   DATABASE_URL=postgresql://postgres:password@192.168.1.100:5432/kacheck_bot
   ```

### Вариант 3: Настройка PostgreSQL для приема внешних подключений

Если база данных должна быть доступна извне:

1. В `postgresql.conf` найдите и раскомментируйте:
   ```
   listen_addresses = '*'
   ```

2. В `pg_hba.conf` добавьте:
   ```
   host    all             all             0.0.0.0/0               md5
   ```

3. Убедитесь, что порт 5432 открыт в firewall.

4. Используйте IP адрес сервера БД в DATABASE_URL.

## Проверка подключения

Для проверки подключения из контейнера:

```bash
docker exec -it kacheck-backend python -c "import psycopg2; psycopg2.connect('$DATABASE_URL')"
```

Или проверьте логи контейнера:
```bash
docker-compose logs backend
```

## Примеры конфигурации

### Локальная разработка (Windows)

**`.env` (в корне проекта):**
```env
DATABASE_URL=postgresql://postgres:1234@host.docker.internal:5432/kacheck_bot
BACKEND_PORT=8000
SECRET_KEY=your-secret-key
```

### Удаленная база данных

**`.env`:**
```env
DATABASE_URL=postgresql://postgres:password@192.168.1.100:5432/kacheck_bot
BACKEND_PORT=8000
SECRET_KEY=your-secret-key
```

### Production (если БД на том же хосте)

Используйте реальный IP или hostname сервера БД:
```env
DATABASE_URL=postgresql://postgres:password@db.example.com:5432/kacheck_bot
```





