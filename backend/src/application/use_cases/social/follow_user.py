from datetime import datetime
from src.domain.repositories.follow_repository import IFollowRepository
from src.domain.entities.follow import Follow, FollowStatus


class FollowUserUseCase:
    """Use case for following a user (creates a pending follow request)."""

    def __init__(self, follow_repository: IFollowRepository):
        self.follow_repository = follow_repository

    def execute(self, follower_id: int, following_id: int) -> Follow:
        """Create a follow request (with PENDING status)."""
        if follower_id == following_id:
            raise ValueError("Cannot follow yourself")

        # Check if already has a request (any status)
        existing = self.follow_repository.get_by_ids(follower_id, following_id)
        if existing:
            if existing.status == FollowStatus.PENDING:
                raise ValueError("Follow request already pending")
            elif existing.status == FollowStatus.APPROVED:
                raise ValueError("Already following this user")
            elif existing.status == FollowStatus.REJECTED:
                # Allow resending request after rejection
                pass

        follow = Follow(
            id=None,
            follower_id=follower_id,
            following_id=following_id,
            created_at=datetime.utcnow(),
            status=FollowStatus.PENDING,
        )

        return self.follow_repository.create(follow)


