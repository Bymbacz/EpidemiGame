from mesa import Model
from simulation.agents.fish_agent import FishTeamAgent
from simulation.rules.fish_rules import FishGameRules
import random

class FishGameModel(Model):
    def __init__(
        self,
        team_names: list[str],
        initial_ocean_fish_population: float = 1000.0,
        initial_sea_fish_population: float = 1000.0,
        ocean_fish_capacity: float = 2000.0,
        sea_fish_capacity: float = 2000.0,
        initial_cash: float = 1000.0
    ):
        super().__init__()
        self.rules = FishGameRules(
            initial_ocean_fish_population=initial_ocean_fish_population,
            initial_sea_fish_population=initial_sea_fish_population,
            ocean_fish_capacity=ocean_fish_capacity,
            sea_fish_capacity=sea_fish_capacity,
            initial_cash=initial_cash
        )
        self.ocean_fish_population = self.rules.initial_ocean_fish_population
        self.sea_fish_population = self.rules.initial_sea_fish_population
        self.teams: list[FishTeamAgent] = []

        for name in team_names:
            agent = FishTeamAgent(self, name)
            self.agents.add(agent)
            self.teams.append(agent)

        self.steps = 0

    def step(self):
        self.agents.do("step")
        self.steps += 1

        # Randomly assign each boat to sea or ocean
        team_boat_assignments = {}
        total_sea_boats = 0
        total_ocean_boats = 0
        for a in self.teams:
            sea_boats = 0
            ocean_boats = 0
            for _ in range(a.boats):
                if random.random() < 0.5:
                    sea_boats += 1
                else:
                    ocean_boats += 1
            team_boat_assignments[a] = {"sea": sea_boats, "ocean": ocean_boats}
            total_sea_boats += sea_boats
            total_ocean_boats += ocean_boats

        # Calculate catch for sea
        sea_catch = min(
            self.sea_fish_population,
            self.rules.catch_factor * total_sea_boats * self.sea_fish_population
        )
        # Calculate catch for ocean
        ocean_catch = min(
            self.ocean_fish_population,
            self.rules.catch_factor * total_ocean_boats * self.ocean_fish_population
        )

        # Distribute catch and cash
        for a in self.teams:
            sea_share = (
                sea_catch * (team_boat_assignments[a]["sea"] / total_sea_boats)
                if total_sea_boats else 0
            )
            ocean_share = (
                ocean_catch * (team_boat_assignments[a]["ocean"] / total_ocean_boats)
                if total_ocean_boats else 0
            )
            a.cash += (sea_share + ocean_share) * self.rules.fish_value

        self.sea_fish_population -= sea_catch
        self.ocean_fish_population -= ocean_catch

        # Growth for both populations
        sea_growth = self.rules.growth_rate * self.sea_fish_population * (
            1 - self.sea_fish_population / self.rules.sea_fish_capacity
        )
        ocean_growth = self.rules.growth_rate * self.ocean_fish_population * (
            1 - self.ocean_fish_population / self.rules.ocean_fish_capacity
        )
        self.sea_fish_population += sea_growth
        self.ocean_fish_population += ocean_growth

    def get_state(self) -> dict:
        return {
            "turn": self.steps,
            "ocean_fish_population": self.ocean_fish_population,
            "sea_fish_population": self.sea_fish_population,
            "teams": [a.to_dict() for a in self.teams]
        }
