""
from api.mixins import CRUDMixin
from db import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Session, relationship


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
