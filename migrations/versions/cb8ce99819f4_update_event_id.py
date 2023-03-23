"""update event id

Revision ID: cb8ce99819f4
Revises: 850ece07e54f
Create Date: 2023-03-23 16:20:53.992391

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb8ce99819f4'
down_revision = '850ece07e54f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_table('event')
    op.create_table(
        'event',
        sa.Column('event_id', sa.UUID, primary_key=True, nullable=False),
        sa.Column('game_id', sa.Integer, nullable=True),
        sa.Column('event_time', sa.DateTime, nullable=False),
        sa.Column('event_type', sa.String(32), nullable=False),
        sa.Column('event_data', sa.JSON, nullable=True),
        sa.Column('published', sa.Boolean, nullable=False, default=False),

        sa.ForeignKeyConstraint(
            columns=['game_id'],
            refcolumns=['game.game_id'],
            name='fk_event_game',
            ondelete='CASCADE'
        ),
    )


def downgrade() -> None:
    op.drop_table('event')
    op.create_table(
        'event',
        sa.Column('event_id', sa.String(36), primary_key=True),
        sa.Column('game_id', sa.Integer, nullable=False),
        sa.Column('event_time', sa.DateTime, nullable=False),
        sa.Column('event_type', sa.String(32), nullable=False),
        sa.Column('event_data', sa.JSON, nullable=True),
        sa.Column('published', sa.Boolean, nullable=False, default=False),

        sa.ForeignKeyConstraint(
            columns=['game_id'],
            refcolumns=['game.game_id'],
            name='fk_event_game',
            ondelete='CASCADE'
        ),
    )