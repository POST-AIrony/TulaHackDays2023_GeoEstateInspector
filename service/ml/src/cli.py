import uvicorn
from core import settings

if __name__ == "__main__":
    uvicorn.run("core.app:app", port=settings.PORT, host=settings.HOST)
