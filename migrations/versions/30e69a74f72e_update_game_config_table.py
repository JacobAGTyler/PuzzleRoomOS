"""update game_config table

Revision ID: 30e69a74f72e
Revises: 1dcaad8984c3
Create Date: 2023-03-22 23:48:29.557926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30e69a74f72e'
down_revision = '1dcaad8984c3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('game_config', sa.Column('duration_minutes', sa.Integer(), nullable=True))
    op.add_column('game_config', sa.Column('parameters', sa.JSON(), nullable=True))

    op.execute("UPDATE game_config SET duration_minutes = 55")
    op.alter_column('game_config', 'duration_minutes', nullable=False)


def downgrade() -> None:
    op.drop_column('game_config', 'parameters')
    op.drop_column('game_config', 'duration_minutes')
