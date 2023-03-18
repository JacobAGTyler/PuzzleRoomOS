"""Update Event Table

Revision ID: 3bd9a1e4f26c
Revises: 459b10a911bc
Create Date: 2023-03-12 17:43:04.982265

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bd9a1e4f26c'
down_revision = '459b10a911bc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('event', 'game_id', nullable=True)


def downgrade() -> None:
    op.alter_column('event', 'game_id', nullable=False)
