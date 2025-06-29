from mesa import Model
# simulation/engine/mesa_engine.py
from simulation.engine.base_engine import BaseEngine

class MesaEngine(BaseEngine):
    """
    Implementacja silnika symulacji dostosowana do Mesa 3.x:
    wykorzystuje AgentSet zamiast przestarzałego mesa.time.
    """
    def __init__(self, model):
        self.model = model
        # Inicjalizacja licznika tur
        self.model.steps = 0

    def initialize(self, model):
        self.model = model
        self.model.steps = 0

    def run_step(self):
        # Aktywacja agentów: każdy agent wykonuje metodę step()
        self.model.agents.do("step")
        # Zwiększenie licznika tur
        self.model.steps += 1
        return self.get_time()

    def get_time(self) -> int:
        return self.model.steps
