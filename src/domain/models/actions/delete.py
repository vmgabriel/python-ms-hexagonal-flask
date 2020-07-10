# Develop: Vmgabriel

# Libraries
from typing import TypeVar, Generic
from abc import ABC, abstractmethod

T = TypeVar('T')

class Delete(ABC, Generic[T]):
    @abstractmethod
    def execute(self, data: T) -> T:
        pass

    @abstractmethod
    def to_query(self, data: T, id: int) -> str:
        pass
