from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_psql
from schemas import LocationBase, LocationResponse, LocationCreate, LocationUpdate
from crud.locations import get_location_by_name, get_location_by_coordinates
from services.locations import find_location
from config.logger import api_logger, api_error_logger

router = APIRouter(prefix="/locations", tags=["Locations"])

# поиск локации из уже существующих по имени или координатам
@router.get("/")
async def get_location_by_name_or_coordinates(
    name: str = None,
    lat: float = None, 
    lon: float = None,
    session: AsyncSession = Depends(get_psql) 
):
    """ 
    TODO: перенести логику в services/locations.py, 
    здесь только вызов функции, и возврат ответа
    """
    if not name and not lat and not lon:
        api_error_logger.error("0 parametrs is given")
        raise HTTPException(status_code=404, detail="0 parametrs is given")
    
    try:
        location = find_location(name=name, lat=lat, lon=lon)
        return location
            
    except Exception as e:
        api_error_logger.error("location is not found, error - {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# router.get("/all")
# async def

# TODO: создание location с использованием только latitude and longitude и OpenStreetMaps API 
router.post()