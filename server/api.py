from fastapi import APIRouter
from server.game_manager import game_manager

router = APIRouter()

@router.post("/game/start")
async def start_game(payload: dict):
    team_list = payload.get("teams") or ["Team A", "Team B"]
    starting_sea_fish = payload.get("starting_sea_fish", 1000)
    starting_ocean_fish = payload.get("starting_ocean_fish", 2000)
    sea_fish_capacity = payload.get("sea_fish_capacity", 2000)
    ocean_fish_capacity = payload.get("ocean_fish_capacity", 2000)
    starting_cash = payload.get("starting_cash", 1000)
    state = game_manager.start_game(
        team_list,
        starting_sea_fish=starting_sea_fish,
        starting_ocean_fish=starting_ocean_fish,
        sea_fish_capacity=sea_fish_capacity,
        ocean_fish_capacity=ocean_fish_capacity,
        starting_cash=starting_cash
    )
    return {
        **state,
        "game_id": game_manager.current_game_id
    }

@router.get("/game/state")
async def get_state():
    return game_manager.get_state()
