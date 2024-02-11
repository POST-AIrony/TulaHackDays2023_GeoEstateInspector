from core import lifespan
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from ml.service import MLService

app = FastAPI(lifespan=lifespan.lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

from ml.controller import ML

app.include_router(ML)


"""
Этот код является частью файла app.py. Он представляет собой middleware для обработки HTTP-запросов. Если в URL запроса содержится "static", то код проверяет параметр "token" и получает пользователя с помощью MLService. Если пользователь является списком, то возвращается JSONResponse с сообщением об ошибке. В противном случае, запрос передается дальше для обработки.
"""


@app.middleware("http")
async def static_ware(request: Request, call_next):
    if "static" in request.url.path:
        print("STATIS GET")
        user_token = request.query_params.get("token")
        user = await MLService.get_user(user_token)
        if isinstance(user, list):
            return JSONResponse(content={"message": user[1]}, status_code=500)

    response = await call_next(request)
    return response
