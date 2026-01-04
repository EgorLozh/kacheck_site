"""add_user_body_metrics_and_weight_height

Revision ID: e6e683e51143
Revises: 96fc41ac88ef
Create Date: 2025-12-28 12:18:30.479650

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6e683e51143'
down_revision: Union[str, None] = '96fc41ac88ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add weight and height columns to users table
    op.add_column('users', sa.Column('weight', sa.Numeric(precision=5, scale=2), nullable=True))
    op.add_column('users', sa.Column('height', sa.Numeric(precision=5, scale=2), nullable=True))
    
    # Create user_body_metrics table
    op.create_table('user_body_metrics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('weight', sa.Numeric(precision=5, scale=2), nullable=True),
    sa.Column('height', sa.Numeric(precision=5, scale=2), nullable=True),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_body_metrics_id'), 'user_body_metrics', ['id'], unique=False)
    op.create_index(op.f('ix_user_body_metrics_user_id'), 'user_body_metrics', ['user_id'], unique=False)
    op.create_index(op.f('ix_user_body_metrics_date'), 'user_body_metrics', ['date'], unique=False)


def downgrade() -> None:
    # Drop user_body_metrics table
    op.drop_index(op.f('ix_user_body_metrics_date'), table_name='user_body_metrics')
    op.drop_index(op.f('ix_user_body_metrics_user_id'), table_name='user_body_metrics')
    op.drop_index(op.f('ix_user_body_metrics_id'), table_name='user_body_metrics')
    op.drop_table('user_body_metrics')
    
    # Remove weight and height columns from users table
    op.drop_column('users', 'height')
    op.drop_column('users', 'weight')




