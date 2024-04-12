from abc import ABC, abstractmethod

class GenericOptimizer(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def optimize(self, f, x0) -> None:
        pass