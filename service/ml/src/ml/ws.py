import uuid
from typing import List

from fastapi import APIRouter, WebSocket, WebSocketException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from ml import models

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


async def заглушка_мл_функции(путь_до_фото):
    return путь_до_фото


@ws_ml.websocket("/ws/{client_id}/{model_type}/{city_title}")
async def websocket_endpoint(
    websocket: WebSocket, client_id: int, model_type: str, city_title: str, token: str
):
    await manager.connect(websocket)

    print("WS CALL")  # TODO: Log this

    # check model type
    if await models.ModelType.exists(title=model_type):
        model = models.ModelType.get(title=model_type)
    else:
        # TODO: Log this
        await websocket.send_text("Model not found")
        await websocket.close()

    # check city
    if await models.CityModel.exists(title=city_title):
        city = models.CityModel.get(title=city_title)
    else:
        # TODO: Log this
        await websocket.send_text("City not found")
        await websocket.close()

    # get user
    user = await MLService.get_user(token)
    if isinstance(user, list):
        await websocket.send_text(res[1])
        await websocket.close()
        await manager.delete(websocket)
    print(user)

    await websocket.send_text("connected")
    while True:
        try:
            photo = await websocket.receive()
            file_name = uuid.uuid4()
            with open(f"static/{file_name}.png", "wb") as f:
                f.write(photo.get("bytes"))
            # https://t.me/FatherKomm ТУТ ФУНКЦИЮ СВОЮ ВПИХИВАЕШЬ КОТОРАЯ ПРИНИМАЕТ f"static/{file_name}.png" и НА ВЫХОД ОТДАЕТ ПУТЬ К ФОТКЕ TODO:
            res = await заглушка_мл_функции(f"/static/{file_name}.png")

            new_photo = models.PhotoFromUser(from_user_id=user.user_id, result_src=res)
            await new_photo.save()

            await websocket.send_text(res)
        except WebSocketException:
            await websocket.close()
            await manager.delete(websocket)
        except TypeError:
            pass
