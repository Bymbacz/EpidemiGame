from abc import ABC, abstractmethod

class BaseGameModel(ABC):
    """
    Abstrakcyjna klasa modelu gry.
    Powinna implementować metodę step() oraz expose stanu.
    """

    @abstractmethod
    def step(self):
        """Wykonaj jedną turę symulacji"""
        pass

    @abstractmethod
    def get_state(self) -> dict:
        """Zwraca serializowalny stan gry"""
        pass
