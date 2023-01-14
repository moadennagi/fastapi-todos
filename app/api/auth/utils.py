"auth module"
import datetime

import jwt

# 90 minutes
JWT_EXP = 90
JWT_SECRET = 'random'

# login : create a token
# refresh the token
# validate the token (authenticate)

def create_jwt(sub: str) -> str:
    exp = datetime.datetime.now() + datetime.timedelta(minutes=JWT_EXP)
    iat = datetime.datetime.now()
    token = jwt.encode(payload={'sub': sub, 'exp': exp, 'iat': iat}, key=JWT_SECRET)
    return token

def validate_jwt(token: str) -> bool:
    try:
        jwt.decode(token, key=JWT_SECRET, algorithms=['HS256'])
    except jwt.DecodeError as e:
        print(e)
        return False
    return True
