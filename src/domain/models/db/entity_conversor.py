# Develop: vmgabriel

# Libraries
import datetime
from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic, Any

T = TypeVar('T')

class Conversor_Type(ABC):
    @abstractmethod
    def str_to(self, data: str) -> str:
        pass

    @abstractmethod
    def int_to(self, data: int) -> str:
        pass

    @abstractmethod
    def datetime_to(self, data: datetime.date) -> str:
        pass

    @abstractmethod
    def bool_to(self, data: bool) -> str:
        pass

    @abstractmethod
    def list_to(self, data: List[Any]) -> str:
        pass

    @abstractmethod
    def keyword_to(self, data: str) -> str:
        pass

    @abstractmethod
    def to_entity(self, type_str: str, data: Any) -> str:
        pass
