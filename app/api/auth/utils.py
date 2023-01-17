"auth module"
import datetime
from datetime import timezone

import jwt
from api.auth.models import User
from api.exceptions import ObjectNotFound
from db import SessionLocal
from sqlalchemy import select
from sqlalchemy.orm import Session

# TODO: add to configuration
# 90 minutes
JWT_EXP = 90
JWT_SECRET = 'random'

def create_jwt(sub: str) -> str:
    exp = datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(hours=JWT_EXP)
    iat = datetime.datetime.now(tz=timezone.utc)
    token = jwt.encode(payload={'sub': sub, 'exp': exp, 'iat': iat}, key=JWT_SECRET)
    return token

def validate_jwt(token: str) -> bool:
    try:
        jwt.decode(token, key=JWT_SECRET, algorithms=['HS256'])
    except jwt.DecodeError as e:
        print(e)
        return False
    return True

def get_user_from_token(token: str, session: Session) -> User:
    user = None
    payload = jwt.decode(token, key=JWT_SECRET, algorithms=['HS256'])
    username = payload['sub']
    q = select(User).where(User.username==username)
    res = session.execute(q).fetchone()
    if not res:
        raise ObjectNotFound
    user = res[0]
    return user