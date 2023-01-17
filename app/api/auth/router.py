from api.auth.dependencies import get_user, get_current_user
from api.auth.schemas import LoginData, Token, UserSchema
from api.auth.utils import create_jwt
from fastapi import APIRouter, Depends

router = APIRouter(tags=['auth',])

@router.post('/login', response_model=Token)
def login(login_data: LoginData, user: UserSchema = Depends(get_user)):
    token_str = create_jwt(user.username)
    token = Token(access_token=token_str)
    return token

@router.get('/me')
def me(current_user: UserSchema = Depends(get_current_user)):
    return current_user
