import pytest
import datetime
import jwt
from fastapi import HTTPException
from datetime import timezone
from api.auth.models import User
from api.auth.utils import JWT_EXP, JWT_SECRET
from sqlalchemy import delete
from sqlalchemy.orm import Session

@pytest.fixture
def jwt_token(user):
    exp = datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(hours=JWT_EXP)
    iat = datetime.datetime.now(tz=timezone.utc)
    token = jwt.encode(payload={'sub': user.username, 'exp': exp, 'iat': iat}, key=JWT_SECRET)
    return token

def test_login_should_return_token(client, user, jwt_token):
    login_data = {'username': 'admin', 'password': 'admin'}
    res = client.post('/login', json=login_data)
    decoded = jwt.decode(jwt_token, key=JWT_SECRET, algorithms=["HS256"])
    assert res.status_code == 200
    assert decoded['sub'] == user.username

def test_route_me(client, user, jwt_token):
    headers = {'Authorization': f'Bearer {jwt_token}'}
    res = client.get('/me', headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data['username'] == user.username
    
def test_route_me_should_raise_exception(client):
    res = client.get('/me')
    assert res.status_code == 401