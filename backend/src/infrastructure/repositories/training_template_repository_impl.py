from typing import Optional, List

from sqlalchemy.orm import Session, joinedload

from src.domain.entities.training_template import TrainingTemplate
from src.domain.entities.implementation_template import ImplementationTemplate
from src.domain.entities.set_template import SetTemplate
from src.domain.repositories.training_template_repository import ITrainingTemplateRepository
from src.infrastructure.database.models.training_template_model import TrainingTemplateModel
from src.infrastructure.database.models.implementation_template_model import ImplementationTemplateModel
from src.infrastructure.database.models.set_template_model import SetTemplateModel


class TrainingTemplateRepositoryImpl(ITrainingTemplateRepository):
    """SQLAlchemy implementation of TrainingTemplate repository (Adapter)."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, template: TrainingTemplate) -> TrainingTemplate:
        """Create a new training template."""
        db_template = TrainingTemplateModel(
            name=template.name,
            description=template.description,
            user_id=template.user_id,
        )
        self.db.add(db_template)
        self.db.flush()

        # Create implementation templates
        for impl_template in template.implementation_templates:
            db_impl_template = ImplementationTemplateModel(
                training_template_id=db_template.id,
                exercise_id=impl_template.exercise_id,
                order_index=impl_template.order_index,
            )
            self.db.add(db_impl_template)
            self.db.flush()

            # Create set templates
            for set_template in impl_template.set_templates:
                db_set_template = SetTemplateModel(
                    implementation_template_id=db_impl_template.id,
                    order_index=set_template.order_index,
                    weight=set_template.weight,
                    reps=set_template.reps,
                )
                self.db.add(db_set_template)

        self.db.commit()
        self.db.refresh(db_template)
        return self._to_entity(db_template)

    def get_by_id(self, template_id: int) -> Optional[TrainingTemplate]:
        """Get training template by ID."""
        db_template = (
            self.db.query(TrainingTemplateModel)
            .options(
                joinedload(TrainingTemplateModel.implementation_templates).joinedload(
                    ImplementationTemplateModel.set_templates
                )
            )
            .filter(TrainingTemplateModel.id == template_id)
            .first()
        )
        return self._to_entity(db_template) if db_template else None

    def get_all(self, user_id: Optional[int] = None, include_system: bool = True) -> List[TrainingTemplate]:
        """Get all training templates, optionally filtered by user."""
        query = self.db.query(TrainingTemplateModel).options(
            joinedload(TrainingTemplateModel.implementation_templates).joinedload(
                ImplementationTemplateModel.set_templates
            )
        )

        if user_id is not None:
            if include_system:
                query = query.filter(
                    (TrainingTemplateModel.user_id == user_id) | (TrainingTemplateModel.user_id.is_(None))
                )
            else:
                query = query.filter(TrainingTemplateModel.user_id == user_id)
        elif not include_system:
            query = query.filter(TrainingTemplateModel.user_id.isnot(None))

        db_templates = query.all()
        return [self._to_entity(t) for t in db_templates]

    def update(self, template: TrainingTemplate) -> TrainingTemplate:
        """Update training template."""
        if template.id is None:
            raise ValueError("Template id is required for update")
        db_template = (
            self.db.query(TrainingTemplateModel).filter(TrainingTemplateModel.id == template.id).first()
        )
        if not db_template:
            raise ValueError(f"Template with id {template.id} not found")

        db_template.name = template.name
        db_template.description = template.description

        # Delete old implementation templates
        self.db.query(ImplementationTemplateModel).filter(
            ImplementationTemplateModel.training_template_id == template.id
        ).delete()

        # Create new implementation templates
        for impl_template in template.implementation_templates:
            db_impl_template = ImplementationTemplateModel(
                training_template_id=db_template.id,
                exercise_id=impl_template.exercise_id,
                order_index=impl_template.order_index,
            )
            self.db.add(db_impl_template)
            self.db.flush()

            for set_template in impl_template.set_templates:
                db_set_template = SetTemplateModel(
                    implementation_template_id=db_impl_template.id,
                    order_index=set_template.order_index,
                    weight=set_template.weight,
                    reps=set_template.reps,
                )
                self.db.add(db_set_template)

        self.db.commit()
        self.db.refresh(db_template)
        return self._to_entity(db_template)

    def delete(self, template_id: int) -> None:
        """Delete training template."""
        db_template = (
            self.db.query(TrainingTemplateModel).filter(TrainingTemplateModel.id == template_id).first()
        )
        if db_template:
            self.db.delete(db_template)
            self.db.commit()

    def _to_entity(self, db_template: TrainingTemplateModel) -> TrainingTemplate:
        """Convert SQLAlchemy model to domain entity."""
        impl_templates = []
        for db_impl_template in db_template.implementation_templates:
            set_templates = []
            for db_set_template in db_impl_template.set_templates:
                set_templates.append(
                    SetTemplate(
                        id=db_set_template.id,
                        implementation_template_id=db_set_template.implementation_template_id,
                        order_index=db_set_template.order_index,
                        weight=float(db_set_template.weight) if db_set_template.weight else None,
                        reps=db_set_template.reps,
                    )
                )
            impl_templates.append(
                ImplementationTemplate(
                    id=db_impl_template.id,
                    training_template_id=db_impl_template.training_template_id,
                    exercise_id=db_impl_template.exercise_id,
                    order_index=db_impl_template.order_index,
                    set_templates=set_templates,
                )
            )

        return TrainingTemplate(
            id=db_template.id,
            name=db_template.name,
            description=db_template.description,
            user_id=db_template.user_id,
            implementation_templates=impl_templates,
            created_at=db_template.created_at,
            updated_at=db_template.updated_at,
        )

