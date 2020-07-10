# Develop vmgabriel

from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic, Any, Tuple

class Db_Connection:
    @abstractmethod
    def get_connection(self) -> Any:
        pass

    @abstractmethod
    def get_cursor(self) -> Any:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def connector(self) -> str:
        pass
