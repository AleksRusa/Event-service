from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_psql
from schemas import LocationBase, LocationResponse, LocationCreate, LocationUpdate
from services.locations import find_location, create_location_by_coordinates
from crud.locations import get_all_locations
from config.logger import api_logger, api_error_logger

router = APIRouter()

# поиск локации из уже существующих по имени или координатам
@router.get("/location")
async def get_location_by_name_or_coordinates(
    name: str = None,
    lat: float = None, 
    lon: float = None,
    session: AsyncSession = Depends(get_psql) 
):
    if not name and not lat and not lon:
        api_error_logger.error("zero parametrs is given")
        raise HTTPException(status_code=404, detail="zero parametrs is given")
    
    try:
        location = await find_location(session=session ,name=name, lat=lat, lon=lon)
        return location
            
    except Exception as e:
        api_error_logger.error(f"location is not found, error - {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/all")
async def get_locations(
    session: AsyncSession = Depends(get_psql)
) -> list[LocationResponse]:
    locations = await get_all_locations(session=session)
    api_logger.info(f"got {len(locations)} locations from db")
    if len(locations) == 0:
        api_error_logger.warning("locations not found")
        raise HTTPException(status_code=404, detail="locations not found")
    return [LocationResponse.model_validate(location) for location in locations]



# TODO: создание location с использованием только latitude and longitude и OpenStreetMaps API 
@router.post("/create_location")
async def create_location(
    name: str,
    lat: float,
    lon: float,
    way_to_start_image: str = None,
    session: AsyncSession = Depends(get_psql)
):
    new_location = await create_location_by_coordinates(name=name, lat=lat, lon=lon, session=session)
    return new_location
    
    