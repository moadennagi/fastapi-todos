""
from pydantic import BaseModel
from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey,
    select, delete
)
from sqlalchemy.orm import Session, relationship
from db.db import Base
from api.dependencies import get_session

# input validation
class TodoBase(BaseModel):
    title: str
    completed: bool = False
    description: str | None = None

class CreateTodo(TodoBase):
    pass

class UpdateTodo(TodoBase):
    pass


class NotFound(Exception):
    pass


class CRUDMixin:
    id: int
    __tablename__: str

    @classmethod
    def get(cls, pk: int, session: Session):
        q = select(cls).where(cls.id == pk)
        res = session.execute(q).fetchone()
        if not res:
            raise NotFound
        obj = res[0]
        return obj

    @classmethod
    def create(cls, data: CreateTodo, session: Session):
        obj = cls(**dict(data))
        session.add(obj)
        session.commit()
        return obj

    @classmethod
    def update(cls, pk: int, data: dict, session: Session):
        q = select(cls).where(cls.id == pk)
        res = session.execute(q).fetchone()
        if not res:
            raise NotFound
        obj = res[0]
        for k, v in data.items():
            if getattr(obj, k) != v:
                setattr(obj, k, v)
        session.commit()
        return obj

    @classmethod
    def all(cls, session: Session):
        q = select(cls)
        res = session.execute(q).fetchall()
        return res

    @classmethod
    def bulk_delete(cls, pks: list[int], session: Session) -> list[int]:
        q = delete(cls).where(cls.id.in_(pks))
        session.execute(q)
        session.commit()
        return pks



class Todo(Base, CRUDMixin):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(400))
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship('User', back_populates='todos')

    def save(self, session: Session):
        session.add(self)
        session.commit()

class User(Base, CRUDMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    superuser = Column(Boolean, default=False)

    todos = relationship('Todo', back_populates='user')

