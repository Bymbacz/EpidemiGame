from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """
    Klasa bazowa agentów.
    """
    @abstractmethod
    def step(self):
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass
