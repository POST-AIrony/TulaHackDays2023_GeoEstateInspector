from fastapi import APIRouter

ML = APIRouter()

from ml.ws import ws_ml

ML.include_router(ws_ml)
