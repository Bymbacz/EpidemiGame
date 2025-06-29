import json
from pathlib import Path

class GameRepository:
    STORAGE_DIR = Path("saved_games")

    def __init__(self):
        self.STORAGE_DIR.mkdir(exist_ok=True)

    def save_state(self, game_id: str, state: dict):
        path = self.STORAGE_DIR / f"{game_id}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)

    def load_state(self, game_id: str) -> dict:
        path = self.STORAGE_DIR / f"{game_id}.json"
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
