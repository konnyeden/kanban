from typing import Dict, List
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, board_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(board_id, []).append(websocket)

    def disconnect(self, board_id: int, websocket: WebSocket):
        if board_id in self.active_connections:
            self.active_connections[board_id] = [ws for ws in self.active_connections[board_id] if ws != websocket]
            if not self.active_connections[board_id]:
                del self.active_connections[board_id]

    async def broadcast(self, board_id: int, message: dict):
        conns = self.active_connections.get(board_id, [])
        for ws in conns:
            try:
                await ws.send_json(message)
            except Exception:
                self.disconnect(board_id, ws)


manager = ConnectionManager()
