"""Game Data

Revision ID: e46ed9ce1e52
Revises: 9a0019407791
Create Date: 2024-04-20 22:17:55.449340

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e46ed9ce1e52'
down_revision = '9a0019407791'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('game', sa.Column('game_data', sa.JSON, key='_game_data'))
    op.alter_column('game', 'game_config_id', nullable=True)


def downgrade() -> None:
    op.drop_column('game', '_game_data')
    op.alter_column('game', 'game_config_id', nullable=False)
