from pydantic import BaseModel


class LoginData(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str

class UserSchema(BaseModel):
    id: int
    username: str
    password: str
    superuser: bool

    class Config:
        orm_mode = True
