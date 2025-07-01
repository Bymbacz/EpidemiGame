from simulation.rules.base_rules import BaseGameRules

class FishGameRules(BaseGameRules):
    def __init__(
        self,
        initial_ocean_fish_population=1000.0,
        initial_sea_fish_population=1000.0,
        ocean_fish_capacity=2000.0,
        sea_fish_capacity=2000.0,
        growth_rate=0.2,
        catch_factor=0.01,
        fish_value=5.0,
        boat_cost=100.0,
        initial_boats=5,
        initial_cash=1000.0,
        max_turns=10
    ):
        super().__init__()
        self.initial_ocean_fish_population = initial_ocean_fish_population
        self.initial_sea_fish_population = initial_sea_fish_population
        self.ocean_fish_capacity = ocean_fish_capacity
        self.sea_fish_capacity = sea_fish_capacity
        self.growth_rate = growth_rate
        self.catch_factor = catch_factor
        self.fish_value = fish_value
        self.boat_cost = boat_cost
        self.initial_boats = initial_boats
        self.initial_cash = initial_cash
        self.max_turns = max_turns
