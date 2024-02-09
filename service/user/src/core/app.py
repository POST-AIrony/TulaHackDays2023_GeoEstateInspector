from core import lifespan
from fastapi import APIRouter, FastAPI

app = FastAPI(lifespan=lifespan.lifespan)

from auth.controller import auth
from user.controller import user

API = APIRouter(prefix="/api")

API.include_router(user, prefix="/user")
API.include_router(auth, prefix="/user/auth")

app.include_router(API)
