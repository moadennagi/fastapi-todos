from api.mixins import CRUDMixin
from db import Base
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import Session, relationship


class User(Base, CRUDMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    superuser = Column(Boolean, default=False)

    todos = relationship('Todo', back_populates='user')

    def save(self, session: Session):
        session.add(self)
        session.commit()
