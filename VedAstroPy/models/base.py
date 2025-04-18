
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict
from enum import Enum

class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"

@dataclass
class GeoLocation:
    name: str
    longitude: float
    latitude: float

@dataclass 
class Time:
    std_time: str  # Format: "HH:MM DD/MM/YYYY +HH:MM"
    location: GeoLocation

@dataclass
class Person:
    person_id: str
    name: str
    notes: str
    birth_time: Time
    gender: Gender
    owner_id: str
    life_event_list: List['LifeEvent']

@dataclass
class LifeEvent:
    person_id: str
    id: str
    name: str
    start_time: Time
    description: str
    nature: str
    weight: str
