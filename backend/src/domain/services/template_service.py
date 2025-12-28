from datetime import datetime

from ..entities.training_template import TrainingTemplate
from ..entities.training import Training, TrainingStatus
from ..entities.implementation_template import ImplementationTemplate
from ..entities.implementation import Implementation
from ..entities.set_template import SetTemplate
from ..entities.set import Set
from ..value_objects.weight import Weight
from ..value_objects.reps import Reps


class TemplateService:
    """Domain service for creating trainings from templates."""

    @staticmethod
    def create_training_from_template(
        template: TrainingTemplate,
        user_id: int,
        date_time: datetime,
    ) -> Training:
        """
        Create a Training entity from a TrainingTemplate.

        Args:
            template: Training template to use
            user_id: ID of the user creating the training
            date_time: Date and time of the training

        Returns:
            New Training entity with implementations based on template
        """
        implementations = []
        for impl_template in template.implementation_templates:
            sets = []
            for set_template in impl_template.set_templates:
                # Create set with template values or default values if not specified
                weight = Weight(set_template.weight if set_template.weight else 0.0)
                reps = Reps(set_template.reps if set_template.reps else 1)
                sets.append(
                    Set(
                        id=None,
                        implementation_id=0,  # Will be set when implementation is saved
                        order_index=set_template.order_index,
                        weight=weight,
                        reps=reps,
                        rest_time=None,
                        duration=None,
                        rpe=None,
                    )
                )

            implementations.append(
                Implementation(
                    id=None,
                    training_id=0,  # Will be set when training is saved
                    exercise_id=impl_template.exercise_id,
                    order_index=impl_template.order_index,
                    sets=sets,
                )
            )

        now = datetime.utcnow()
        return Training(
            id=None,
            user_id=user_id,
            training_template_id=template.id,
            date_time=date_time,
            duration=None,
            notes=None,
            status=TrainingStatus.PLANNED,
            implementations=implementations,
            created_at=now,
            updated_at=now,
        )



