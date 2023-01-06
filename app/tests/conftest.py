import pytest

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from db.db import Base
from main import app


engine = create_engine("sqlite+pysqlite:///tests.sqlite", future=True)
SessionTest = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="session")
def client() -> Generator:
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="session")
def session() -> Generator:
    try:
        session = SessionTest()
        yield session
    finally:
        session.close()
