from mesa import Model
from simulation.agents.fish_agent import FishTeamAgent
from simulation.rules.fish_rules import FishGameRules

class FishGameModel(Model):
    def __init__(self, team_names: list[str]):
        super().__init__()
        self.rules = FishGameRules()
        self.fish_population = self.rules.initial_fish_population
        self.teams: list[FishTeamAgent] = []

        # Now pass only (model, name) to each agent
        for name in team_names:
            agent = FishTeamAgent(self, name)
            self.agents.add(agent)
            self.teams.append(agent)

        self.steps = 0

    def step(self):
        self.agents.do("step")
        self.steps += 1

        total_boats = sum(a.boats for a in self.teams)
        catch = min(self.fish_population,
                    self.rules.catch_factor * total_boats * self.fish_population)
        for a in self.teams:
            share = catch * (a.boats / total_boats) if total_boats else 0
            a.cash += share * self.rules.fish_value

        self.fish_population -= catch
        growth = self.rules.growth_rate * self.fish_population * (
            1 - self.fish_population / self.rules.carrying_capacity
        )
        self.fish_population += growth

    def get_state(self) -> dict:
        return {
            "turn": self.steps,
            "fish_population": self.fish_population,
            "teams": [a.to_dict() for a in self.teams]
        }
