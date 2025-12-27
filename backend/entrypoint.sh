#!/bin/bash
set -e

echo "Waiting for database connection..."
# Try to connect to database (max 30 attempts = 30 seconds)
max_attempts=30
attempt=0
until python -c "import psycopg2; psycopg2.connect('$DATABASE_URL')" 2>/dev/null; do
  attempt=$((attempt + 1))
  if [ $attempt -ge $max_attempts ]; then
    echo "Failed to connect to database after $max_attempts attempts"
    echo "Please check DATABASE_URL: ${DATABASE_URL%%@*}" # Show URL without password
    exit 1
  fi
  echo "Database is unavailable - sleeping (attempt $attempt/$max_attempts)"
  sleep 1
done

echo "Database is up - executing migrations"
cd /app
alembic upgrade head

echo "Starting application"
exec uvicorn src.presentation.main:app --host 0.0.0.0 --port ${BACKEND_PORT:-8000}

