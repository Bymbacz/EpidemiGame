from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from server.game_manager import game_manager

router = APIRouter()

@router.websocket("/ws/game")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    game_manager.register(ws)
    try:
        await ws.send_json(game_manager.get_state())
        while True:
            data = await ws.receive_json()
            if data.get("action") == "end_turn":
                state = game_manager.process_turn()
                await game_manager.broadcast(state)
    except WebSocketDisconnect:
        game_manager.unregister(ws)
