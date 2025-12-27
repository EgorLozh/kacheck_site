# Load environment variables BEFORE any imports that might need them
import os
from pathlib import Path
from dotenv import load_dotenv

# .env file is in the parent directory (project root)
# __file__ is backend/src/infrastructure/migrations/env.py
# Go up: migrations -> infrastructure -> src -> backend -> project_root
migrations_dir = Path(__file__).parent  # backend/src/infrastructure/migrations
infrastructure_dir = migrations_dir.parent  # backend/src/infrastructure
src_dir = infrastructure_dir.parent  # backend/src
backend_dir = src_dir.parent  # backend
project_root = backend_dir.parent  # project root
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Import base and models
from src.infrastructure.database.base import Base
from src.infrastructure.database.models import *  # noqa: F401, F403

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set sqlalchemy.url from environment variable if present
database_url = os.getenv("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

