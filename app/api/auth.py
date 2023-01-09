"auth module"
import uuid
import jwt

from typing import Union
from dataclasses import dataclass


class NotFound(Exception):
    pass

class InvalidCredentials(Exception):
    pass
