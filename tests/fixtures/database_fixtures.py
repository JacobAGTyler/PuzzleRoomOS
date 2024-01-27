import pytest

from sqlalchemy import create_engine, create_mock_engine, engine
from sqlalchemy.orm import scoped_session, sessionmaker


def sql_logger(sql, *multiparams, **params):
    print(sql.compile(dialect=engine.dialect))


@pytest.fixture
def mock_engine():
    return create_mock_engine('postgresql+psycopg2://', sql_logger)


@pytest.fixture(scope='session', autouse=True)
def db_engine():
    """yields a SQLAlchemy engine which is suppressed after the test session"""
    db_url = 'sqlite:///:memory:'
    engine_ = create_engine(db_url, echo=True)

    yield engine_

    engine_.dispose()


@pytest.fixture(scope='session', autouse=True)
def db_session_factory(db_engine):
    """returns a SQLAlchemy scoped session factory"""
    return scoped_session(sessionmaker(bind=db_engine))


@pytest.fixture(scope='function')
def db_session(db_session_factory):
    """yields a SQLAlchemy connection which is rolled back after the test"""
    session_ = db_session_factory()

    yield session_

    session_.rollback()
    session_.close()