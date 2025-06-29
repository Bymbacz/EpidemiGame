from fastapi import APIRouter
from server.game_manager import game_manager

router = APIRouter()

@router.post("/game/start")
async def start_game(payload: dict):
    # Domyślnie tworzymy dwie drużyny, jeśli nie podano listy
    team_list = payload.get("teams") or ["Team A", "Team B"]
    state = game_manager.start_game(team_list)
    return {
        **state,
        "game_id": game_manager.current_game_id
    }

@router.get("/game/state")
async def get_state():
    return game_manager.get_state()
