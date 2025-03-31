import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config.config import settings

try:
    Database_URL = os.getenv("Database_URL")
except:
    Database_URL = settings.Database_URL


async_engine = create_async_engine(
    url=Database_URL,
    echo=False,
)

async_session = async_sessionmaker(async_engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_psql():
    db = async_session()
    try:
        yield db
    finally:
        await db.close()