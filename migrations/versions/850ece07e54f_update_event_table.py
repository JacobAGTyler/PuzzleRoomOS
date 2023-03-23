"""update event table

Revision ID: 850ece07e54f
Revises: 30e69a74f72e
Create Date: 2023-03-23 00:31:08.865579

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '850ece07e54f'
down_revision = '30e69a74f72e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('event', sa.Column('published', sa.Boolean, nullable=False, default=False))


def downgrade() -> None:
    op.drop_column('event', 'published')
