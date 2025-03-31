from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config.config import settings

async_engine = create_async_engine(
    url=settings.Database_URL,
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