from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List

T = TypeVar("T")

class Repository(Generic[T], ABC):
    @abstractmethod
    def get(self, id: int) -> T:
        raise NotImplementedError
    
    @abstractmethod
    def get_all(self) -> List[T]:
        raise NotImplementedError
    
    @abstractmethod
    def add(self, obj: T) -> T:
        raise NotImplementedError
    
    @abstractmethod
    def add(self, obj: T) -> T:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, obj: T) -> T:
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, id: int) -> None:
        raise NotImplementedError