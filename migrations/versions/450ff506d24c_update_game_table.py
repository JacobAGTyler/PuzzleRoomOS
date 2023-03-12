"""Update Game Table

Revision ID: 450ff506d24c
Revises: c2c00970f25b
Create Date: 2023-03-12 14:48:05.388284

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '450ff506d24c'
down_revision = 'c2c00970f25b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('game', sa.Column('end_time', sa.DateTime, nullable=True))
    op.add_column('game', sa.Column('ended', sa.Boolean, nullable=True, default=False))

    op.execute("UPDATE game SET ended = false")

    op.alter_column('game', 'ended', nullable=False)


def downgrade() -> None:
    op.drop_column('game', 'end_time')
    op.drop_column('game', 'ended')
