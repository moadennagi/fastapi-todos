import pytest
import jwt
from api.auth.utils import create_jwt, validate_jwt, get_user_from_token
from api.auth.utils import JWT_EXP, JWT_SECRET

from api.auth.models import User
from sqlalchemy import delete

def test_create_jwt_should_return_token_with_valid_data():
    name = 'foobar'
    token = create_jwt(name)
    decoded = jwt.decode(token, key=JWT_SECRET, algorithms=['HS256'])
    assert decoded['sub'] == name

def test_get_user_from_token(user, session):
    token = create_jwt(user.username)
    user_obj = get_user_from_token(token, session)
    assert user == user_obj

def test_create_jwt_should_fail_on_expired_tokens():
    ...

def test_validate_jwt_should_return_true_on_valid_data():
    ...

def test_validate_jwt_should_return_false_on_invalid_data():
    ...