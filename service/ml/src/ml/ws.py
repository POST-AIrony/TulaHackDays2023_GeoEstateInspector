import uuid
from typing import List

from fastapi import APIRouter, WebSocket, WebSocketException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .service import MLService

html = ""
with open("index.html", "r") as f:
    html = f.read()

ws_ml = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def broadcast(self, data: str):
        for connection in self.connections:
            await connection.send_text(data)

    async def delete(self, w: WebSocket):
        self.connections.remove(w)


manager = ConnectionManager()


@ws_ml.get("/")
async def get():
    return HTMLResponse(html)


@ws_ml.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int, token: str):
    print("WS CALL")
    await manager.connect(websocket)
    res = await MLService.get_user(token)
    if isinstance(res, list):
        await websocket.send_text(res[1])
        await websocket.close()
        await manager.delete(websocket)

    await websocket.send_text("connected")
    while True:
        try:
            photo = await websocket.receive()
            file_name = uuid.uuid4()
            with open(f"static/{file_name}.png", "wb") as f:
                f.write(photo.get("bytes"))

            await websocket.send_text(f"static/{file_name}.png")
        except WebSocketException:
            await websocket.close()
            await manager.delete(websocket)
        except TypeError:
            pass
