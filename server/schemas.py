from pydantic import BaseModel
from typing import List

class TeamState(BaseModel):
    name: str
    boats: int
    cash: float

class GameState(BaseModel):
    turn: int
    fish_population: float
    teams: List[TeamState]
