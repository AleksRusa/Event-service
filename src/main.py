import os
import sys
from contextlib import asynccontextmanager

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.logger import db_logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_logger.info("event_service запущен")
    yield
    db_logger.info("event_service завершён") 

app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    uvicorn.run(
        app="src.main:app",
        reload=True,
    )