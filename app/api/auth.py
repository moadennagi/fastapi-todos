"auth module"
import uuid
import jwt

from typing import Union
from dataclasses import dataclass


class NotFound(Exception):
    pass

class InvalidCredentials(Exception):
    pass

# @dataclass
# class User:
#     pk: str
#     username: str
#     password: str
#     superuser: bool

#     @classmethod
#     def authenticate(cls, username: str, password: str):
#         user = list(filter(lambda x: x.username == username, users))
#         if not user:
#             raise NotFound
#         user = user[0]
#         if user.password != password:
#             raise InvalidCredentials
#         return user

# users = [User(pk=str(uuid.uuid4()), username='admin', password='admin', superuser=True),]

