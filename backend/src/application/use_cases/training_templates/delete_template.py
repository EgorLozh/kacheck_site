from src.domain.repositories.training_template_repository import ITrainingTemplateRepository


class DeleteTemplateUseCase:
    """Use case for deleting a training template."""

    def __init__(self, template_repository: ITrainingTemplateRepository):
        self.template_repository = template_repository

    def execute(self, template_id: int, user_id: int) -> None:
        """Delete a training template."""
        # Get existing template
        template = self.template_repository.get_by_id(template_id)
        if not template:
            raise ValueError(f"Template with id {template_id} not found")

        # Check ownership
        if template.user_id != user_id:
            raise ValueError("You don't have permission to delete this template")

        self.template_repository.delete(template_id)



