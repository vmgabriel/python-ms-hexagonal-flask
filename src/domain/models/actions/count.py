# Develop: Vmgabriel

# Libraries
from abc import ABC, abstractmethod

class Count(ABC):
    @abstractmethod
    def execute(self, query: str) -> int:
        pass
