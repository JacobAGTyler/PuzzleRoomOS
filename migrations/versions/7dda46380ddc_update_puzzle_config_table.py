"""update puzzle_config table

Revision ID: 7dda46380ddc
Revises: cb8ce99819f4
Create Date: 2023-03-23 23:01:53.766282

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7dda46380ddc'
down_revision = 'cb8ce99819f4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('puzzle_config', sa.Column('puzzle_reference', sa.String(length=255), nullable=True))
    op.add_column('puzzle_config', sa.Column('definition', sa.JSON(), nullable=True))
    op.drop_column('puzzle_config', 'description')


def downgrade() -> None:
    op.add_column('puzzle_config', sa.Column('description', sa.String(255), nullable=True))
    op.drop_column('puzzle_config', 'definition')
    op.drop_column('puzzle_config', 'puzzle_reference')
