from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any


class Settings(BaseSettings):
    """Application settings."""

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ENVIRONMENT: str = "development"
    BACKEND_PORT: int = 8000

    class Config:
        # .env file is in the project root (parent of backend directory)
        # __file__ is backend/src/infrastructure/settings.py
        infrastructure_dir = Path(__file__).parent  # backend/src/infrastructure
        src_dir = infrastructure_dir.parent  # backend/src
        backend_dir = src_dir.parent  # backend
        project_root = backend_dir.parent  # project root
        env_file = str(project_root / ".env")
        case_sensitive = True
        extra = "allow"  # Разрешаем дополнительные поля


settings = Settings()