# Develop: Vmgabriel

# Libraries
from typing import TypeVar, Generic, Any, List
from abc import ABC, abstractmethod

# Interfaces
from domain.models.filter_interface import Filter_Interface

T = TypeVar('T')

class Get_All(ABC, Generic[T]):
    @abstractmethod
    def execute(
            self,
            limit: int,
            offset: int
    ) -> List[T]:
        pass
