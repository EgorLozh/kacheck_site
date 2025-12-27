from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from src.infrastructure.database.base import Base
from src.infrastructure.database.models import *  # noqa: F401, F403


class Database:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def create_tables(self):
        """Create all tables."""
        Base.metadata.create_all(bind=self.engine)

    def get_session(self) -> Generator[Session, None, None]:
        """Get database session."""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()


# Global database instance (will be initialized in main.py)
database: Database | None = None


def init_db(db: Database) -> None:
    """Initialize global database instance."""
    global database
    database = db


def get_db() -> Generator[Session, None, None]:
    """Dependency for FastAPI to get database session."""
    if database is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    yield from database.get_session()

