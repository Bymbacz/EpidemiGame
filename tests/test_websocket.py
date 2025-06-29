import pytest
from fastapi.testclient import TestClient
from server.main import app

@pytest.mark.asyncio
async def test_ws_turn_flow():
    client = TestClient(app)
    with client.websocket_connect("/ws/game") as ws:
        init = ws.receive_json()
        assert init["turn"] == 0
        ws.send_json({"action": "end_turn"})
        updated = ws.receive_json()
        assert updated["turn"] == 1
