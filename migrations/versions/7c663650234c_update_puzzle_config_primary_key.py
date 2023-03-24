"""update puzzle_config primary key

Revision ID: 7c663650234c
Revises: 7dda46380ddc
Create Date: 2023-03-23 23:31:35.926506

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c663650234c'
down_revision = '7dda46380ddc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('puzzle_config', sa.Column('puzzle_code', sa.String(32), nullable=False, default='DEFAULT'))


def downgrade() -> None:
    op.drop_column('puzzle_config', 'puzzle_code')
