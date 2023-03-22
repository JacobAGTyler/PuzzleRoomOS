"""update game table

Revision ID: 22c4214d5d89
Revises: e729e40c3cc8
Create Date: 2023-03-22 22:32:24.127568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22c4214d5d89'
down_revision = 'e729e40c3cc8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('game', 'game_ref', new_column_name='game_reference')


def downgrade() -> None:
    op.alter_column('game', 'game_reference', new_column_name='game_ref')
