"""Create Event Table

Revision ID: 459b10a911bc
Revises: 450ff506d24c
Create Date: 2023-03-12 15:24:06.113851

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '459b10a911bc'
down_revision = '450ff506d24c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'event',
        sa.Column('event_id', sa.String(36), primary_key=True),
        sa.Column('game_id', sa.Integer, nullable=False),
        sa.Column('event_time', sa.DateTime, nullable=False),
        sa.Column('event_type', sa.String(32), nullable=False),
        sa.Column('event_data', sa.JSON, nullable=True),

        sa.ForeignKeyConstraint(
            columns=['game_id'],
            refcolumns=['game.game_id'],
            name='fk_event_game',
            ondelete='CASCADE'
        ),
    )


def downgrade() -> None:
    op.drop_table('event')
