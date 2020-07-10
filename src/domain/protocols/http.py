# Develop Vmgabriel

# Libraries
from flask import Blueprint
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

class HttpProtocol(ABC):
    @abstractmethod
    def get_blueprint(self) -> Blueprint:
        pass
