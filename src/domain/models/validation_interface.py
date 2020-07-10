# Develop vmgabriel

from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic, Any

T = TypeVar('T')

class Validate_Interface(ABC, Generic[T]):
    @abstractmethod
    def validate_object(self, data: Any) -> (str, T):
        pass

    @abstractmethod
    def validate_object_update(self, data: Any) -> (str, T):
        pass
