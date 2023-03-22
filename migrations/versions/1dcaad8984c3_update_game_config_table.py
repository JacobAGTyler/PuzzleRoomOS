"""update game_config table

Revision ID: 1dcaad8984c3
Revises: 22c4214d5d89
Create Date: 2023-03-22 22:42:52.060246

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1dcaad8984c3'
down_revision = '22c4214d5d89'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('game_config', sa.Column('config_reference', sa.String(255), nullable=True))

    op.execute("UPDATE game_config SET config_reference = 'default';")
    op.alter_column('game_config', 'config_reference', nullable=False)


def downgrade() -> None:
    op.drop_column('game_config', 'config_reference')
