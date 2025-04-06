from typing import Optional
from datetime import datetime

from pydantic import BaseModel

class LocationBase(BaseModel):
    name: str
    country: str
    city: str
    region: str
    latitude: float
    longitude: float

    class Config:
        from_attributes = True 

class LocationCreate(LocationBase):
    way_to_start_image: Optional[str]
    creation_datetime: datetime

class LocationUpdate(LocationBase):
    country: Optional[str]
    city: Optional[str]
    region: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    way_to_start_image: Optional[str]

class LocationResponse(LocationUpdate):
    name: str

