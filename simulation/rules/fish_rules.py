from simulation.rules.base_rules import BaseGameRules

class FishGameRules(BaseGameRules):
    def __init__(self):
        super().__init__()
        # Parametry populacji ryb
        self.initial_fish_population = 1000.0
        self.growth_rate = 0.2
        self.carrying_capacity = 2000.0
        # Parametry ekonomiczne
        self.catch_factor = 0.01
        self.fish_value = 5.0
        self.boat_cost = 100.0
        # Parametry gry
        self.initial_boats = 5
        self.initial_cash = 1000.0
        self.max_turns = 10
