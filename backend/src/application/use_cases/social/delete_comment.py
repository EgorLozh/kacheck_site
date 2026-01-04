from src.domain.repositories.training_comment_repository import ITrainingCommentRepository


class DeleteCommentUseCase:
    """Use case for deleting a comment."""

    def __init__(self, comment_repository: ITrainingCommentRepository):
        self.comment_repository = comment_repository

    def execute(self, comment_id: int, user_id: int) -> None:
        """Delete a comment (only by owner)."""
        comment = self.comment_repository.get_by_id(comment_id)
        if not comment:
            raise ValueError("Comment not found")

        if comment.user_id != user_id:
            raise ValueError("Cannot delete comment: not the owner")

        self.comment_repository.delete(comment_id)


