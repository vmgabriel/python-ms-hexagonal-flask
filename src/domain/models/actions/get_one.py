# Develop: Vmgabriel

# Libraries
from typing import TypeVar, Generic
from abc import ABC, abstractmethod

T = TypeVar('T')

class Get_One(ABC, Generic[T]):
    @abstractmethod
    def execute(self, id: int) -> T:
        pass

    @abstractmethod
    def to_query(self, data: int) -> str:
        pass
