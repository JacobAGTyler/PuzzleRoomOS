"""update puzzle table

Revision ID: 9a0019407791
Revises: 7c663650234c
Create Date: 2023-03-24 11:16:59.347374

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a0019407791'
down_revision = '7c663650234c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('puzzle', sa.Column('prerequisites', sa.JSON, nullable=True))
    op.add_column('puzzle', sa.Column('solutions', sa.JSON, nullable=True))
    op.add_column('puzzle', sa.Column('triggers', sa.JSON, nullable=True))


def downgrade() -> None:
    pass
