import pytest

from sqlalchemy import create_mock_engine, engine


def sql_logger(sql, *multiparams, **params):
    print(sql.compile(dialect=engine.dialect))


@pytest.fixture
def mock_engine():
    return create_mock_engine('postgresql+psycopg2://', sql_logger)
