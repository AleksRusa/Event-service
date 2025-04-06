# TODO: запросы к бд связынные с локацией

from fastapi import HTTPException
from sqlalchemy import select, insert ,and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from database.models import Locations
from config.logger import db_error_logger, db_logger



async def get_location_by_name(name: str, session: AsyncSession):
    try:
        query = select(Locations).where(Locations.name == name)
        result = await session.execute(query)
        location = result.scalars().first()
        if location:
            db_logger.info(f"[DB] Found location with name: {name}")
        else:
            db_logger.info(f"[DB] No location found with name: {name}")
        return location
    except SQLAlchemyError as e:
        db_error_logger.error(f"[DB ERROR] Failed to get location by name '{name}': {e}")
        raise

EPSILON = 0.05

async def get_location_by_coordinates(lat: float, lon: float, session: AsyncSession):
    try:
        query = select(Locations).where(
            and_(
                Locations.latitude.between(lat - EPSILON, lat + EPSILON), 
                Locations.longitude.between(lon - EPSILON, lon + EPSILON)
            )
        )
        result = await session.execute(query)
        location = result.scalars().first()
        if location:
            db_logger.info(f"[DB] Found location near lat={lat}, lon={lon}")
        else:
            db_logger.info(f"[DB] No location found near lat={lat}, lon={lon}")
        return location
    except SQLAlchemyError as e:
        db_error_logger.error(f"[DB ERROR] Failed to get location by coordinates lat={lat}, lon={lon}: {e}")
        raise

async def get_all_locations(session: AsyncSession):
    try:
        query = select(Locations)
        result = await session.execute(query)
        locations = result.scalars().all()
        db_logger.info(f"[DB] Retrieved {len(locations)} locations")
        return locations
    
    except SQLAlchemyError as e:
        db_error_logger.error(f"[DB ERROR] Failed to get all locations: {e}")
        raise

async def create_new_location(payload: dict, session: AsyncSession):
    try:
        query = insert(Locations).values(**payload).returning(Locations)
        result = await session.execute(query)
        await session.commit()
        new_location = result.scalar_one()
        db_logger.info("created new location")
        return new_location
    
    except IntegrityError as e:
        await session.rollback()
        db_error_logger.error(f"location already exists - {e}")
        raise HTTPException(status_code=400, detail="Location already exists")
    
    except Exception as e:
        db_error_logger.error(f"Internal server error - {e}")
        await session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

