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

echo "Database is up - granting permissions on public schema"
# Grant permissions on public schema (required for PostgreSQL 15+)
python << 'PYEOF'
import psycopg2
from urllib.parse import urlparse
from psycopg2 import sql
import os
import sys

# Parse DATABASE_URL
database_url = os.environ.get("DATABASE_URL")
if not database_url:
    print("Warning: DATABASE_URL not set, skipping permission grant")
    sys.exit(0)

parsed = urlparse(database_url)
dbname = parsed.path[1:]  # Remove leading '/'
user = parsed.username
password = parsed.password
host = parsed.hostname
port = parsed.port or 5432

if not user:
    print("Warning: Could not extract username from DATABASE_URL, skipping permission grant")
    sys.exit(0)

try:
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Grant usage and create privileges on public schema
    # Use sql.Identifier for safe identifier quoting
    user_ident = sql.Identifier(user)
    cursor.execute(
        sql.SQL("GRANT USAGE ON SCHEMA public TO {};").format(user_ident)
    )
    cursor.execute(
        sql.SQL("GRANT CREATE ON SCHEMA public TO {};").format(user_ident)
    )
    
    # Also grant privileges on existing tables (if any)
    cursor.execute(
        sql.SQL("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO {};").format(user_ident)
    )
    cursor.execute(
        sql.SQL("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO {};").format(user_ident)
    )
    
    cursor.close()
    conn.close()
    print("Permissions granted successfully")
except Exception as e:
    print(f"Warning: Could not grant permissions: {e}")
    print("Continuing anyway...")
PYEOF

echo "Executing migrations"
cd /app
alembic upgrade head

echo "Starting application"
exec uvicorn src.presentation.main:app --host 0.0.0.0 --port ${BACKEND_PORT:-8000}

