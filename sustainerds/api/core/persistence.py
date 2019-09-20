import uuid
from abc import abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional, Text

from typing_extensions import Protocol


class PersistenceError(Exception):
    """Placeholder Exception for all persistence related topics."""


@dataclass
class StorageResult:
    """Simple rust-like Result object which needs to be tuned more.
    
    #TODO: somehow replace the `__post_init__() function with build- / compile time
           logic.
    """

    ok: Optional[Dict] = None
    err: Optional[Exception] = None

    def __post_init__(self):
        if not self.ok and not self.err:
            raise ValueError("Neither ok nor err are set.")

        if self.ok and self.err:
            raise ValueError("Only one value of ok or err can be set.")


class PersistenceApi(Protocol):
    """Interface definition for persistence wrappers"""

    @abstractmethod
    def store(self, entity: Text, data: Dict) -> StorageResult:
        raise NotImplementedError

    @abstractmethod
    def fetch(self, entity: Text, id: Text) -> StorageResult:
        raise NotImplementedError


class InMemoryPersistence:
    """Simple In-Memory persistence functionality, complying with the `PersistenceApi`
    protocol.
    """

    data: Dict = dict()

    def store(self, entity: Text, data: Dict) -> StorageResult:
        _id = uuid.uuid4()
        self.data.setdefault(entity, {})
        self.data[entity].setdefault(_id, data)
        data.update(id=_id)

        return StorageResult(ok=data)

    def fetch(self, entity: Text, _id: Text) -> StorageResult:
        iid = uuid.UUID(_id)
        try:
            return StorageResult(ok=self.data[entity][iid])
        except KeyError as ex:
            return StorageResult(err=ex)
