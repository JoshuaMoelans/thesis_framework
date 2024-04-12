from abc import ABC, abstractmethod

class GenericOptimizer(ABC):
    @abstractmethod
    def __init__(self) -> None:
        return NotImplementedError

    @abstractmethod
    def optimize(self) -> None:
        return NotImplementedError