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
    """Класс ConnectionManager предназначен для управления соединениями через WebSocket.

    При инициализации класса создается пустой список self.connections, который будет использоваться для хранения подключенных WebSocket-соединений.

    Метод connect асинхронно принимает WebSocket-соединение и добавляет его в список self.connections.

    Метод broadcast асинхронно отправляет данные всем подключенным WebSocket-соединениям.

    Метод delete асинхронно удаляет указанное WebSocket-соединение из списка self.connections.

    Примечание: для работы с WebSocket-соединениями рекомендуется использовать библиотеку aiohttp.
    """

    def __init__(self):
        """Инициализирует новый экземпляр класса ConnectionManager, создавая пустой список self.connections."""
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Асинхронно принимает WebSocket-соединение и добавляет его в список self.connections."""
        await websocket.accept()
        self.connections.append(websocket)

    async def broadcast(self, data: str):
        """Асинхронно отправляет данные всем WebSocket-соединениям, подключенным к экземпляру ConnectionManager."""
        for connection in self.connections:
            await connection.send_text(data)

    async def delete(self, w: WebSocket):
        """Асинхронно удаляет указанное WebSocket-соединение из списка self.connections."""
        self.connections.remove(w)


manager = ConnectionManager()


@ws_ml.get("/")
async def get():
    return HTMLResponse(html)


@ws_ml.websocket("/ws/{client_id}/{model_type}")
async def websocket_endpoint(
    websocket: WebSocket, client_id: int, model_type: str, token: str
):
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
            # https://t.me/FatherKomm ТУТ ФУНКЦИЮ СВОЮ ВПИХИВАЕШЬ КОТОРАЯ ПРИНИМАЕТ f"static/{file_name}.png" и НА ВЫХОД ОТДАЕТ ПУТЬ К ФОТКЕ TODO:
            await websocket.send_text(f"static/{file_name}.png")
        except WebSocketException:
            await websocket.close()
            await manager.delete(websocket)
        except TypeError:
            pass
