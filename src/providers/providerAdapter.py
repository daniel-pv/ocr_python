
from abc import ABC, abstractmethod

class ProviderAdapter(ABC):
 
    @abstractmethod
    def read(self, source: str) -> list:
        """Present provider"""
        pass
    
    @abstractmethod
    def write(self, list: list, source: str) -> None:
        """Present provider"""
        pass