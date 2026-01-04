from src.domain.repositories.follow_repository import IFollowRepository
from src.domain.entities.follow import Follow, FollowStatus


class ApproveFollowRequestUseCase:
    """Use case for approving a follow request."""

    def __init__(self, follow_repository: IFollowRepository):
        self.follow_repository = follow_repository

    def execute(self, follower_id: int, following_id: int) -> Follow:
        """Approve a follow request."""
        # Get the follow request
        follow = self.follow_repository.get_by_ids(follower_id, following_id)
        if not follow:
            raise ValueError("Follow request not found")

        if follow.status != FollowStatus.PENDING:
            raise ValueError(f"Follow request is not pending (current status: {follow.status.value})")

        # Update status to APPROVED
        updated_follow = self.follow_repository.update_status(follower_id, following_id, FollowStatus.APPROVED)
        if not updated_follow:
            raise ValueError("Failed to approve follow request")

        return updated_follow

