# Develop: Vmgabriel

# Libraries
from typing import TypeVar, Generic, Any
from abc import ABC, abstractmethod

T = TypeVar('T')

class Update(ABC, Generic[T]):
    @abstractmethod
    def execute(self, id: int, data: T) -> T:
        pass

    @abstractmethod
    def to_entity(self, data: T) -> str:
        pass

    @abstractmethod
    def to_query(self, data: T, id: int) -> str:
        pass
