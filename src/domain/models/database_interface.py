# Develop vmgabriel

from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic, Any

from domain.models.filter_interface import Attribute_Filter, Filter_Interface

T = TypeVar('T')

class Database_Interface(ABC, Generic[T]):
    @abstractmethod
    def count(self, query: str) -> int:
        pass

    @abstractmethod
    def get_all(self, limit: int, offset: int) -> (List[T], int):
        pass

    @abstractmethod
    def filter(
            self,
            filters: Filter_Interface,
            attributes: List[Attribute_Filter],
            joins: Any,
            limit: int,
            offset: int
    ) -> (List[T], int):
        pass

    @abstractmethod
    def get_one(self, id: int) -> T:
        pass

    @abstractmethod
    def create(self, data: T) -> T:
        pass

    @abstractmethod
    def update(self, data: T, id: int) -> T:
        pass

    @abstractmethod
    def delete(self, id: int) -> T:
        pass

    @abstractmethod
    def builder(self, definition: str) -> None:
        pass
