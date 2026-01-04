from typing import Optional, List
from sqlalchemy.orm import Session

from src.domain.repositories.follow_repository import IFollowRepository
from src.domain.entities.follow import Follow, FollowStatus
from src.infrastructure.database.models.follow_model import FollowModel


class FollowRepositoryImpl(IFollowRepository):
    """SQLAlchemy implementation of Follow repository (Adapter)."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, follow: Follow) -> Follow:
        """Create a new follow relationship."""
        db_follow = FollowModel(
            follower_id=follow.follower_id,
            following_id=follow.following_id,
            status=follow.status,
        )
        self.db.add(db_follow)
        self.db.commit()
        self.db.refresh(db_follow)
        return self._to_entity(db_follow)

    def delete(self, follower_id: int, following_id: int) -> None:
        """Delete a follow relationship."""
        db_follow = (
            self.db.query(FollowModel)
            .filter(
                FollowModel.follower_id == follower_id,
                FollowModel.following_id == following_id,
            )
            .first()
        )
        if db_follow:
            self.db.delete(db_follow)
            self.db.commit()

    def get_by_ids(self, follower_id: int, following_id: int) -> Optional[Follow]:
        """Get follow relationship by follower and following IDs."""
        db_follow = (
            self.db.query(FollowModel)
            .filter(
                FollowModel.follower_id == follower_id,
                FollowModel.following_id == following_id,
            )
            .first()
        )
        return self._to_entity(db_follow) if db_follow else None

    def get_followers(self, user_id: int) -> List[Follow]:
        """Get all users following a user."""
        db_follows = (
            self.db.query(FollowModel)
            .filter(FollowModel.following_id == user_id)
            .all()
        )
        return [self._to_entity(f) for f in db_follows]

    def get_following(self, user_id: int) -> List[Follow]:
        """Get all users a user is following."""
        db_follows = (
            self.db.query(FollowModel)
            .filter(FollowModel.follower_id == user_id)
            .all()
        )
        return [self._to_entity(f) for f in db_follows]

    def update_status(self, follower_id: int, following_id: int, status: FollowStatus) -> Optional[Follow]:
        """Update follow request status."""
        db_follow = (
            self.db.query(FollowModel)
            .filter(
                FollowModel.follower_id == follower_id,
                FollowModel.following_id == following_id,
            )
            .first()
        )
        if not db_follow:
            return None
        
        db_follow.status = status
        self.db.commit()
        self.db.refresh(db_follow)
        return self._to_entity(db_follow)

    def get_following_approved(self, user_id: int) -> List[Follow]:
        """Get all users a user is following with approved status."""
        db_follows = (
            self.db.query(FollowModel)
            .filter(
                FollowModel.follower_id == user_id,
                FollowModel.status == FollowStatus.APPROVED
            )
            .all()
        )
        return [self._to_entity(f) for f in db_follows]

    def _to_entity(self, db_follow: FollowModel) -> Follow:
        """Convert SQLAlchemy model to domain entity."""
        return Follow(
            id=db_follow.id,
            follower_id=db_follow.follower_id,
            following_id=db_follow.following_id,
            created_at=db_follow.created_at,
            status=db_follow.status,
        )


