from os import getenv
from alembic.config import Config
from alembic import command


class SetupHandler:
    @staticmethod
    def initialise_database():
        # Load the Alembic configuration
        alembic_cfg = Config("alembic.ini")

        connection_string = getenv(
            key='DATABASE_URL',
            default='postgresql+psycopg2://jacob:jacob@localhost:5432/puzzle_room_os'
        )

        alembic_cfg.set_main_option("sqlalchemy.url", connection_string)

        # Run the migrations
        command.upgrade(alembic_cfg, "head")
