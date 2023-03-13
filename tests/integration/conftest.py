import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from app import settings

# mock the database URL

from app.db import config

print("Loading conftest.py")


@pytest.fixture(scope="session")
def engine():
    """Create a new database for testing."""
    print("Creating database")
    engine = create_engine("sqlite:///:memory:", echo=True)
    config.Base.metadata.create_all(engine)
    yield engine
    config.Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def session(engine):
    """Create a new session for each test."""
    print("Creating session")
    connection = engine.connect()
    transaction = connection.begin()

    session = sessionmaker(bind=connection)()
    yield session

    session.close()
    transaction.rollback()
    connection.close()
