import uuid
from typing import List

from fastapi import FastAPI, WebSocket, WebSocketException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image, ImageDraw, ImageFont

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


html = ""
with open("index.html", "r") as f:
    html = f.read()


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


@app.get("/")
async def get():
    return HTMLResponse(html)


async def prosecc_photo_ml(photo_path):
    img = Image.open(photo_path)
    draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype(
        r"WadeSansLightStd.otf",
        22,
    )
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text(
        (0, 0),
        "Sample Text ALO ALO ALO ALO ALO ALO ALO",
        (255, 0, 0),
        font=font,
    )
    nn = uuid.uuid4()
    img.save(f"static/{nn}.png")
    return f"static/{nn}.png"


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int, token: str):
    await manager.connect(websocket)
    print(token)
    while True:
        try:
            photo = await websocket.receive()
            print(photo)
            n = uuid.uuid4()
            print(n)
            with open(f"static/{n}.png", "wb") as f:
                f.write(photo.get("bytes"))

            await websocket.send_text(await prosecc_photo_ml(f"static/{n}.png"))
        except WebSocketException as e:
            await websocket.close()
            await manager.delete(websocket)
        except TypeError:
            pass


# from cmd - > uvicorn ws:app
