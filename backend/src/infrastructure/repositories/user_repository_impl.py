from typing import Optional, List
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import or_

from src.domain.entities.user import User
from src.domain.repositories.user_repository import IUserRepository
from src.infrastructure.database.models.user_model import UserModel


class UserRepositoryImpl(IUserRepository):
    """SQLAlchemy implementation of User repository (Adapter)."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        """Create a new user."""
        db_user = UserModel(
            email=user.email,
            username=user.username,
            hashed_password=user.hashed_password,
            weight=user.weight,
            height=user.height,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return self._to_entity(db_user)

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_entity(db_user) if db_user else None

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        db_user = self.db.query(UserModel).filter(UserModel.email == email).first()
        return self._to_entity(db_user) if db_user else None

    def update(self, user: User) -> User:
        """Update user."""
        if user.id is None:
            raise ValueError("User id is required for update")
        db_user = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if not db_user:
            raise ValueError(f"User with id {user.id} not found")

        db_user.email = user.email
        db_user.username = user.username
        db_user.hashed_password = user.hashed_password
        db_user.weight = user.weight
        db_user.height = user.height
        db_user.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(db_user)
        return self._to_entity(db_user)

    def delete(self, user_id: int) -> None:
        """Delete user."""
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if db_user:
            self.db.delete(db_user)
            self.db.commit()

    def search_by_username(self, username_query: str, limit: int = 20) -> List[User]:
        """Search users by username (case-insensitive partial match)."""
        query = self.db.query(UserModel).filter(
            UserModel.username.ilike(f"%{username_query}%")
        ).limit(limit)
        db_users = query.all()
        return [self._to_entity(user) for user in db_users]

    @staticmethod
    def _to_entity(db_user: UserModel) -> User:
        """Convert SQLAlchemy model to domain entity."""
        return User(
            id=db_user.id,
            email=db_user.email,
            username=db_user.username,
            hashed_password=db_user.hashed_password,
            weight=float(db_user.weight) if db_user.weight is not None else None,
            height=float(db_user.height) if db_user.height is not None else None,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
        )


