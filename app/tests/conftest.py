from typing import Generator

import pytest
from api.auth.models import User
from api.dependencies import get_session
from db import Base
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import Session, sessionmaker

engine = create_engine("sqlite+pysqlite:///tests.sqlite", future=True)
SessionTest = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def get_test_db() -> Generator:
    try:
        session = SessionTest()
        yield session
    finally:
        session.close()

@pytest.fixture(scope="session")
def session():
    session = next(get_test_db())
    return session

@pytest.fixture(scope="session")
def client(session) -> Generator:
    app.dependency_overrides[get_session] = get_test_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.setdefault

@pytest.fixture()
def user(session: Session):
    obj = User(username='admin', password='admin', superuser=False)
    obj = obj.save(session=session)
    yield obj
    q = delete(User).where(User.username=='admin')
    session.execute(q)
    session.commit()