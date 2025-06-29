from abc import ABC, abstractmethod

class BaseEngine(ABC):
    """
    Abstrakcyjny interfejs silnika symulacji.
    Implementacje: MesaEngine, SimPyEngine itd.
    """

    @abstractmethod
    def initialize(self, model):
        """Przygotuj silnik do symulacji modelu"""
        pass

    @abstractmethod
    def run_step(self):
        """Wykonaj jedną turę symulacji"""
        pass

    @abstractmethod
    def get_time(self) -> int:
        """Zwraca aktualny numer tury"""
        pass