import pytest
from api.auth.dependencies import get_user
from api.auth.models import User
from api.auth.schemas import LoginData
from api.exceptions import ObjectNotFound
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

def test_get_user_should_return_userschema(user, session: Session):
    login_data = LoginData(username='admin', password='admin')
    user = get_user(login_data, db=session)
    assert user

def test_get_user_should_raise_notfound(session: Session):
    with pytest.raises(ObjectNotFound):
        login_data = LoginData(username='admin', password='admin')
        get_user(login_data, db=session)
