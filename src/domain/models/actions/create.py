# Develop: Vmgabriel

# Libraries
from typing import TypeVar, Generic
from abc import ABC, abstractmethod

T = TypeVar('T')

class Create(ABC, Generic[T]):
    @abstractmethod
    def execute(self, data: T) -> T:
        pass

    @abstractmethod
    def to_entity(self, data: T) -> (str, str):
        pass

    @abstractmethod
    def to_query(self, data: T) -> str:
        pass
