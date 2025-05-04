from fastapi import FastAPI, Query, Body
import uvicorn
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth
from src.config import settings
from src.database import *

app = FastAPI()

app.include_router(router_auth)
app.include_router(router_hotels)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)