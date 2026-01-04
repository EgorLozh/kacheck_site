"""add_status_to_follows

Revision ID: 941750e54664
Revises: 4bff305f623d
Create Date: 2026-01-04 21:29:34.846519

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '941750e54664'
down_revision: Union[str, None] = '4bff305f623d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum type with uppercase values to match Python enum
    follow_status_enum = sa.Enum('PENDING', 'APPROVED', 'REJECTED', name='followstatus')
    follow_status_enum.create(op.get_bind(), checkfirst=True)
    
    # Add status column with default value 'PENDING'
    op.add_column('follows', sa.Column('status', follow_status_enum, nullable=False, server_default='PENDING'))
    
    # Update existing rows to 'APPROVED' status (for backward compatibility)
    op.execute("UPDATE follows SET status = 'APPROVED'::followstatus")


def downgrade() -> None:
    op.drop_column('follows', 'status')
    op.execute("DROP TYPE IF EXISTS followstatus")





