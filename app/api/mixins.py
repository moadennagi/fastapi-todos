from api.exceptions import ObjectNotFound
from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from db import SessionLocal


class CRUDMixin:
    """Crud queries
    """

    @classmethod
    def get(cls, pk: int, session: Session):
        q = select(cls).where(cls.id == pk)
        res = session.execute(q).fetchone()
        if not res:
            raise ObjectNotFound
        obj = res[0]
        return obj

    @classmethod
    def create(cls, data: BaseModel, session: Session):
        obj = cls(**dict(data))
        session.add(obj)
        session.commit()
        return obj

    @classmethod
    def update(cls, pk: int, data: dict, session: Session):
        q = select(cls).where(cls.id == pk)
        res = session.execute(q).fetchone()
        if not res:
            raise ObjectNotFound
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
