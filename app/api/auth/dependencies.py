from api.auth.models import User
from api.auth.schemas import LoginData, UserSchema
from api.dependencies import get_session
from api.exceptions import ObjectNotFound
from api.auth.utils import get_user_from_token
from fastapi import Depends, Request, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_user(login_data: LoginData, db: Session = Depends(get_session)) -> UserSchema:
    username = login_data.username
    q = select(User).where(User.username==username)
    res = db.execute(q).fetchone()
    if not res:
        raise ObjectNotFound
    res = res[0]
    user = UserSchema.from_orm(res)
    return user

def get_auth(request: Request):
    auth_headers = request.headers.get('Authorization')
    if not auth_headers:
        raise HTTPException(status_code=401)
    try:
        token = auth_headers.split(' ')[1]
    except IndexError:
        raise HTTPException(status_code=401)
    return token

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)) -> UserSchema:
    user = get_user_from_token(token, db)
    user_schema = UserSchema.from_orm(user)
    return user_schema