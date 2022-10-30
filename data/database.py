from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
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


def retrieve_entity(entity_id: int, entity_class, session: Session):
    entity_filter = {f"{snakecase(entity_class.__class__.__name__)}_id": entity_id}
    entity = session.query(entity_class).filter_by(**entity_filter).first()
    session.close()
    return entity
