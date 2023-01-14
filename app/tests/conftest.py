from typing import Generator

import pytest
from api.dependencies import get_session
from db import Base
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine("sqlite+pysqlite:///tests.sqlite", future=True)
SessionTest: sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def get_test_db() -> Generator[Session, None, None]:
    try:
        session: Session = SessionTest()
        yield session
    finally:
        session.close()

@pytest.fixture(scope="session")
def session() -> Generator:
    try:
        session = SessionTest()
        yield session
    finally:
        session.close()

@pytest.fixture(scope="session")
def client(session) -> Generator:
    app.dependency_overrides[get_session] = get_test_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.setdefault
