"""create puzzle table

Revision ID: e729e40c3cc8
Revises: 3bd9a1e4f26c
Create Date: 2023-03-22 02:04:53.459678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e729e40c3cc8'
down_revision = '3bd9a1e4f26c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'puzzle',
        sa.Column('puzzle_id', sa.Integer, primary_key=True),
        sa.Column('game_id', sa.Integer, sa.ForeignKey('game.game_id')),
        sa.Column('puzzle_config_id', sa.Integer, sa.ForeignKey('puzzle_config.puzzle_config_id')),
        sa.Column('puzzle_reference', sa.String(255)),
        sa.Column('solved', sa.Boolean, default=False),
        sa.Column('solve_time', sa.DateTime, nullable=True),
        sa.Column('data', sa.JSON, nullable=True)
    )

    op.create_foreign_key(
        constraint_name='fk_puzzle_game',
        source_table='puzzle',
        local_cols=['game_id'],
        referent_table='game',
        remote_cols=['game_id'],
        ondelete='CASCADE'
    )

    op.create_foreign_key(
        constraint_name='fk_puzzle_puzzle_config',
        source_table='puzzle',
        local_cols=['puzzle_config_id'],
        referent_table='puzzle_config',
        remote_cols=['puzzle_config_id'],
        ondelete='RESTRICT'
    )


def downgrade() -> None:
    op.drop_table('puzzle')
