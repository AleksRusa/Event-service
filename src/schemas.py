from typing import Optional
from datetime import datetime

from pydantic import BaseModel

class LocationBase(BaseModel):
    country: str
    city: str
    area: str
    latitude: float
    logitude: float

class LocationCreate(LocationBase):
    way_to_start_image: Optional[str]
    creation_datetime: datetime

class LocationUpdate(BaseModel):
    country: Optional[str]
    city: Optional[str]
    area: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    way_to_start_image: Optional[str]

class LocationResponse(LocationBase):
    way_to_start_image: Optional[str]

