# TODO: запросы к бд связынные с локацией

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Locations


async def get_location_by_name(name: str, session: AsyncSession):
    query = select(Locations).where(Locations.name == name)
    result = await session.execute(query)

async def get_location_by_coordinates(lat: float, lon: float, db: AsyncSession):
    pass