from sqlalchemy import create_engine, select
from sqlalchemy.engine import Engine
from sqlalchemy.engine.row import Row

from sqlalchemy.orm import Session
from caseconverter import snakecase

connection_string = "postgresql+psycopg2://jacob:jacob@localhost:5432/puzzle_room_os"


def get_engine() -> Engine:
    engine = create_engine(connection_string, echo=True, future=True)
    return engine


def get_connection(engine: Engine) -> Session:
    return Session(engine, future=True)


def save_entity(entity, session: Session):
    session.add(entity)


def retrieve_entity(entity_id: int, entity_class: type, session: Session):
    entity_id_name = f'{snakecase(entity_class.__name__)}_id'
    statement = select(entity_class).where(getattr(entity_class, entity_id_name) == entity_id)
    result: Row = session.execute(statement).first()

    return result.__getitem__(0)


def retrieve_all(entity_class, session: Session):
    statement = select(entity_class)
    result: list[Row] = session.execute(statement).all()
    return result
