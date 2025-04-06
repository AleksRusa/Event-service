from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import LocationBase, LocationResponse, LocationCreate, LocationUpdate
from crud.locations import get_location_by_name, get_location_by_coordinates
from config.logger import api_logger, api_error_logger


async def find_location(
    session: AsyncSession,
    name: str = None, 
    lat: float = None,
    lon: float = None,
)-> LocationResponse:
    if name:
        location = await get_location_by_name(name=name, session=session)
        if not location:
            api_error_logger.error("location {name} is not found, error - {e}")
            raise HTTPException(status_code=404, detail="Location with {name} is not found")
        api_logger.info(f"location {name} is found")
        return await LocationResponse(**location)
    
    if lat and lon:
        location = await get_location_by_coordinates(lat=lat, lon=lon, session=session)
        if not location:
            api_error_logger.error("location with coordinates {lat}, {lon} is not found")
            raise HTTPException(status_code=404, detail="Location with coordinates {lat}, {lon}  is not found")
        api_logger.info(f"location coordinates {lat}, {lon}  is found")
        return await LocationResponse(**location)