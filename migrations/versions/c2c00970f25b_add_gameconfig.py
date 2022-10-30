"""Add GameConfig

Revision ID: c2c00970f25b
Revises: 45c2600f8e10
Create Date: 2022-10-29 20:24:43.117486

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c2c00970f25b'
down_revision = '45c2600f8e10'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('game_config', sa.Column('name', sa.String(255), nullable=False))
    op.add_column('game_config', sa.Column('version', sa.Integer, nullable=False))
    op.add_column('game_config', sa.Column('description', sa.String(255), nullable=True))
    op.add_column('game_config', sa.Column('author', sa.String(255), nullable=True))
    op.add_column('game_config', sa.Column('author_url', sa.String(255), nullable=True))
    op.add_column('game_config', sa.Column('game_license', sa.String(255), nullable=True))
    op.add_column('game_config', sa.Column('game_url', sa.String(255), nullable=True))

    op.create_table(
        'puzzle_config',
        sa.Column('puzzle_config_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('game_config_id', sa.Integer, nullable=False),
        sa.Column('setup', sa.JSON, nullable=True),
        sa.Column('description', sa.String(255), nullable=True),
    )

    op.create_foreign_key(
        constraint_name='fk_puzzle_config_game_config',
        source_table='puzzle_config',
        local_cols=['game_config_id'],
        referent_table='game_config',
        remote_cols=['game_config_id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    op.drop_constraint('fk_puzzle_config_game_config', 'puzzle_config', type_='foreignkey')
    op.drop_table('puzzle_config')

    op.drop_column('game_config', 'game_url')
    op.drop_column('game_config', 'game_license')
    op.drop_column('game_config', 'author_url')
    op.drop_column('game_config', 'author')
    op.drop_column('game_config', 'description')
    op.drop_column('game_config', 'version')
    op.drop_column('game_config', 'name')
