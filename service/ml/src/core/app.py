from core import lifespan
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

app = FastAPI(lifespan=lifespan.lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

from ml.controller import ML

app.include_router(ML)


@app.middleware("http")
async def static_ware(request: Request, call_next):
    if "static" in request.url.path:
        print("STATIS GET")
    response = await call_next(request)
    return response
