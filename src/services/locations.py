from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import LocationBase, LocationResponse, LocationCreate, LocationUpdate
from crud.locations import (
    get_location_by_name, 
    get_location_by_coordinates, 
    create_new_location
)
from utils.geo import reverse_geocode
from config.logger import api_logger, api_error_logger, db_logger, db_error_logger


async def find_location(
    session: AsyncSession,
    name: str = None, 
    lat: float = None,
    lon: float = None,
)-> LocationResponse:
    if name:
        location = await get_location_by_name(name=name, session=session)
        if not location:
            api_error_logger.warning(f"location {name} is not found")
            raise HTTPException(status_code=404, detail=f"Location with {name} is not found")
        api_logger.info(f"location {name} is found")
        return LocationResponse.model_validate(location)
    
    if lat and lon:
        location = await get_location_by_coordinates(lat=lat, lon=lon, session=session)
        api_logger.info(f"locations with coordinates {lat}, {lon} is found")
        if not location:
            api_error_logger.warning(f"location with coordinates {lat}, {lon} is not found")
            raise HTTPException(status_code=404, detail=f"Location with coordinates {lat}, {lon}  is not found")
        api_logger.info(f"location coordinates {lat}, {lon}  is found")
        return LocationResponse.model_validate(location)
    
async def create_location_by_coordinates(
    name: str,
    lat: float,
    lon: float, 
    session: AsyncSession,
    way_to_start_image: str = None,
) -> LocationResponse:
    location_info = reverse_geocode(lat, lon)
    db_logger.info(f"location info from OpenStreetMap - {location_info}")
    location_info["name"] = name
    location_info["way_to_start_image"] = way_to_start_image
    new_location = await create_new_location(payload=location_info, session=session)
    return LocationResponse.model_validate(new_location)