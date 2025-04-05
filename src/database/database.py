import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config.pg_config import settings

async_Database_URL = os.getenv("async_Database_URL") or settings.async_Database_URL

async_engine = create_async_engine(
    url=async_Database_URL,
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