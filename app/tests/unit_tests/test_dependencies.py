import pytest
import datetime
import jwt

from fastapi import Request
from datetime import timezone
from api.auth.dependencies import get_user, get_current_user
from api.auth.models import User
from api.auth.schemas import LoginData
from api.exceptions import ObjectNotFound
from sqlalchemy import delete
from sqlalchemy.orm import Session

from api.auth.utils import JWT_EXP, JWT_SECRET


@pytest.fixture
def req():
    request = Request(scope={},)

def test_get_user_should_return_userschema(user, session: Session):
    login_data = LoginData(username='admin', password='admin')
    user = get_user(login_data, db=session)
    assert user

def test_get_user_should_raise_notfound(session: Session):
    with pytest.raises(ObjectNotFound):
        login_data = LoginData(username='admin', password='admin')
        get_user(login_data, db=session)
