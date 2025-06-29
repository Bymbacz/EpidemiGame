from mesa import Agent
from simulation.agents.base_agent import BaseAgent

class FishTeamAgent(Agent, BaseAgent):
    """Agent reprezentujący zespół/kraj w grze."""

    def __init__(self, model, name: str):
        # In Mesa 3.0 unique_id is auto-assigned; super() takes only the model
        super().__init__(model)
        self.name = name
        self.boats = model.rules.initial_boats
        self.cash = model.rules.initial_cash

    def step(self):
        # Przykładowa automatyczna logika
        if self.model.steps % 5 == 0 and self.cash >= self.model.rules.boat_cost:
            self.cash -= self.model.rules.boat_cost
            self.boats += 1

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "boats": self.boats,
            "cash": self.cash
        }
