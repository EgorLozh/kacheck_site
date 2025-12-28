"""add_in_progress_status_to_training

Revision ID: 96fc41ac88ef
Revises: 7fc343c3337b
Create Date: 2025-12-28 11:34:00.021938

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96fc41ac88ef'
down_revision: Union[str, None] = '7fc343c3337b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add IN_PROGRESS value to trainingstatus enum
    # Note: In PostgreSQL, ALTER TYPE ... ADD VALUE cannot be executed inside a transaction block
    # We need to execute this outside of Alembic's transaction
    # Use op.execute() with autocommit=True or execute directly on connection
    connection = op.get_bind()
    
    # Check if IN_PROGRESS already exists
    result = connection.execute(sa.text("""
        SELECT EXISTS (
            SELECT 1 FROM pg_enum 
            WHERE enumlabel = 'IN_PROGRESS' 
            AND enumtypid = (SELECT oid FROM pg_type WHERE typname = 'trainingstatus')
        )
    """))
    
    exists = result.scalar()
    
    if not exists:
        # For PostgreSQL, we need to execute ALTER TYPE outside transaction
        # This is a workaround - Alembic will still try to wrap it in a transaction
        # So we'll use a different approach: execute via connection with autocommit
        connection.execute(sa.text("COMMIT"))
        connection.execute(sa.text("ALTER TYPE trainingstatus ADD VALUE 'IN_PROGRESS'"))
        # Start a new transaction for Alembic
        connection.execute(sa.text("BEGIN"))


def downgrade() -> None:
    # PostgreSQL doesn't support removing enum values directly
    # This would require recreating the enum type, which is complex
    # For now, we'll leave it as a no-op
    # In production, you might want to create a new enum type and migrate data
    pass


