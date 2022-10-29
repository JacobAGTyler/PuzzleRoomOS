"""create game table

Revision ID: 45c2600f8e10
Revises:
Create Date: 2022-09-28 15:16:43.476519

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45c2600f8e10'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'game_config',
        sa.Column('game_config_id', sa.Integer, primary_key=True)
    )

    op.create_table(
        'game',
        sa.Column('game_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('game_ref', sa.String(255), nullable=False),
        sa.Column('game_config_id', sa.Integer, nullable=False),
        sa.Column('started', sa.Boolean, nullable=False),
        sa.Column('start_time', sa.DateTime, nullable=True)
    )

    op.create_foreign_key(
        constraint_name='fk_game_game_config',
        source_table='game',
        local_cols=['game_config_id'],
        referent_table='game_config',
        remote_cols=['game_config_id'],
        ondelete='RESTRICT'
    )


def downgrade() -> None:
    op.drop_constraint('fk_game_game_config', 'game', type_='foreignkey')
    op.drop_table('game')
    op.drop_table('game_config')
