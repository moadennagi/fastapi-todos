from api.auth.models import User
from api.auth.schemas import LoginData, UserSchema
from api.dependencies import get_session
from api.exceptions import ObjectNotFound
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session


def get_user(login_data: LoginData, db: Session = Depends(get_session)) -> UserSchema:
    username = login_data.username
    q = select(User).where(User.username==username)
    res = db.execute(q).fetchone()
    if not res:
        raise ObjectNotFound
    res = res[0]
    user = UserSchema.from_orm(res)
    return user
