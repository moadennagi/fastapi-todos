import pytest
from api.auth.models import User
from sqlalchemy import delete
from sqlalchemy.orm import Session


@pytest.fixture()
def user(session: Session):
    user = User(username='admin', password='admin', superuser=False)
    user = user.save(session=session)
    yield user
    q = delete(User).where(User.username=='admin')
    session.execute(q)
    session.commit()

def test_login_should_return_token(user, client):
    login_data = {'username': 'admin', 'password': 'admin'}
    res = client.post('/login', json=login_data)
    print(res)
