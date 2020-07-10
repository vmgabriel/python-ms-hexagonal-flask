# Develop: Vmgabriel

# Libraries
from typing import TypeVar, Generic, Any, List
from abc import ABC, abstractmethod

# Interfaces
from domain.models.filter_interface import Filter_Interface, Attribute_Filter, Column_Filter

T = TypeVar('T')

class Filter(ABC, Generic[T]):
    @abstractmethod
    def execute(
            self,
            filters: Filter_Interface,
            attributes: List[Attribute_Filter],
            joins: Any,
            limit: int,
            offset: int
    ) -> (List[T], str):
        pass

    @abstractmethod
    def convert_column(self, column_filter: Column_Filter) -> str:
        pass

    @abstractmethod
    def convert_filter(self, filters: Filter_Interface) -> str:
        pass

    @abstractmethod
    def convert_attributes(
            self,
            attributes: List[Attribute_Filter],
            is_count: bool = False
    ) -> str:
        pass

    @abstractmethod
    def convert_joins(self, joins: Any) -> str:
        pass

    @abstractmethod
    def definitor(self) -> str:
        pass
