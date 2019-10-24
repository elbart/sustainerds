import uuid
from typing import Dict, Optional, Text

from sqlalchemy import Column, String

from sustainerds.api.core.persistence import PersistenceApi, PersistenceError
from sustainerds.api.persistence import Base


class UserDbModel(Base):

    __tablename__ = "user"

    email = Column(String(500))
    password = Column(String(500))


class User:
    """Central user model"""

    __id: Optional[uuid.UUID] = None
    email: Text
    password: Text
    __persistence: PersistenceApi
    __dirty: bool

    def __init__(self, persistence: PersistenceApi):
        self.__persistence = persistence

    @property
    def id(self):
        return self.__id

    def register(self, email, password):
        self.email = email
        self.password = password
        self.__dirty = True

    def save(self):
        data = dict(email=self.email, password=self.password)
        res = self.__persistence.store("User", data)

        if res.err:
            raise PersistenceError(res.err)

        self.__id = res.ok["id"]
        self.__dirty = False

    def load(self, id: str):
        res = self.__persistence.fetch("User", id)

        if res.err:
            raise PersistenceError(res.err)

        if res.ok:
            d: Dict = res.ok

            self.__id = d["id"]
            self.email = d["email"]
            self.password = d["password"]

    def to_dict(self):
        return dict(id=str(self.id), email=self.email, password=self.password)
