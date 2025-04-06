from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Enum as SQLAlchemyEnum, String, Text, CheckConstraint, ForeignKey, text, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import EmailStr

from database.database import Base

class TypeEnum (str, Enum):
    COMPETITION = "соревнование"
    TRAINING_CAMP = "тренировочный старт"

class StatusEnum(str, Enum):
    TRAINING = "тренировочный"
    LOCAL = "местный"
    REGION = "региональный"
    INTERREGION = "межрегиональные"
    ALL_RUSSIA = "всероссийские"


class Event_Programm(Base):
    __tablename__ = "event_programms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    time: Mapped[datetime] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    
class Locations(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    country: Mapped[str] = mapped_column(String(50), default="Россия")
    city: Mapped[str] = mapped_column(String(50), default="Москва")
    area: Mapped[Optional[str]] # optional
    way_to_start_image: Mapped[Optional[str]] # как добраться до старта 
    latitude: Mapped[float] = mapped_column(nullable=False, unique=True) 
    longitude: Mapped[float] = mapped_column(nullable=False, unique=True)
    creation_datetime: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), nullable=False)

class ParticipantGroups(Base): # уже готовые группы
    __tablename__ = "participant_groups"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    min_age: Mapped[int]
    max_age: Mapped[int]
    created_by_id: Mapped[int]

    __table_args__ = (
        CheckConstraint("min_age >= 0 AND min_age <= 100", name="min_age_check"),
        CheckConstraint("max_age >= 0 AND max_age <= 100", name="max_age_check"),
        CheckConstraint("min_age <= max_age", name="age_range_check"),
    )

class Event(Base): # карты и результаты будут связаны с событием через event_id в собственном сервисе
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    type: Mapped[TypeEnum] = mapped_column(SQLAlchemyEnum(TypeEnum), nullable=False)
    description: Mapped[str]
    start_time: Mapped[datetime]
    status: Mapped[StatusEnum] = mapped_column(SQLAlchemyEnum(StatusEnum), nullable=False)
    event_logo_path: Mapped[str] = mapped_column(String(255), nullable=False)
    programm_id: Mapped[int] = mapped_column(ForeignKey("event_programms.id"))
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))
    organizer_id: Mapped[int] # из cookies
    organizer_info: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True) # информация от организатора
    
    participant_groups: Mapped[list["ParticipantGroups"]] = relationship(
        secondary="event_participant_groups",
    )

    event_programm: Mapped["Event_Programm"] = relationship("Event_Programm", back_populates="event")

class EventParticipantGroup(Base):
    __tablename__ = "event_participant_groups"

    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("participant_groups.id"))

    __table_args__ = (PrimaryKeyConstraint("event_id", "group_id"),)
