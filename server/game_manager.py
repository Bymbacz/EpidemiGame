# server/game_manager.py

import json
from typing import List, Optional
from fastapi import WebSocket
from uuid import uuid4

from simulation.models.fish_game import FishGameModel
from server.schemas import GameState
from server.game_repository import GameRepository

class GameManager:
    def __init__(self):
        self.repo = GameRepository()
        self.game: Optional[FishGameModel] = None
        self.clients: List[WebSocket] = []
        # Tu inicjalizujemy current_game_id, żeby nie bylo AttributeError
        self.current_game_id: Optional[str] = None

    def start_game(self, team_names: list[str], game_id: str = None) -> dict:
        if game_id:
            state = self.repo.load_state(game_id)
            # zakładamy, że FishGameModel.from_dict istnieje
            self.game = FishGameModel.from_dict(state)
            self.current_game_id = game_id
        else:
            self.game = FishGameModel(team_names)
            # generujemy nowe ID dla tej gry
            self.current_game_id = str(uuid4())
        return self.get_state()

    def get_state(self) -> dict:
        return self.game.get_state()

    def register(self, ws: WebSocket):
        self.clients.append(ws)

    def unregister(self, ws: WebSocket):
        self.clients.remove(ws)

    async def broadcast(self, state: dict):
        for ws in self.clients:
            await ws.send_json(state)

    def process_turn(self) -> dict:
        if not self.game:
            return {}
        # jeśli już przekroczyliśmy limit, nic nie rób
        if self.game.steps >= self.game.rules.max_turns:
            return self.get_state()
        # w normalnym wypadku zrób jeden krok
        self.game.step()
        state = self.get_state()
        self.repo.save_state(self.current_game_id, state)
        return state

# Singleton
game_manager = GameManager()
