
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from models.base import Person, Time, GeoLocation
from models.database import PersonDB, EventDB, engine
from core.calculator import Calculator
from typing import List, Dict
import uuid

app = FastAPI()

@app.post("/api/Calculate/AddPerson")
async def add_person(
    location: str, 
    birth_time: str,  # Format: "HH:MM" (24-hour format, e.g. "14:30")
    birth_date: str,  # Format: "DD/MM/YYYY" (e.g. "25/12/1990")
    person_name: str, 
    gender: str, 
    notes: str, 
    owner_id: str = "cdupadhyay"
):
    """Add a new person record.
    
    Args:
        location: Location name (e.g. "New York")
        birth_time: Time in 24-hour format "HH:MM" (e.g. "14:30")
        birth_date: Date in format "DD/MM/YYYY" (e.g. "25/12/1990") 
        person_name: Full name
        gender: Gender ("Male" or "Female")
        notes: Additional notes
        owner_id: Owner ID (defaults to "cdupadhyay")
    """
    try:
        # Parse location string for lat/long
        lat, lon = 0.0, 0.0  # You'll need to implement geocoding
        
        # Parse birth time and date
        time_str = f"{birth_time} {birth_date}"  # Format: "HH:MM DD/MM/YYYY"
        birth_datetime = datetime.strptime(time_str, "%H:%M %d/%m/%Y")
        
        # Create database session
        session = Session(engine)
        
        # Create person record
        person_id = str(uuid.uuid4())
        db_person = PersonDB(
            id=person_id,
            name=person_name,
            gender=gender,
            owner_id=owner_id,
            notes=notes,
            latitude=lat,
            longitude=lon,
            location_name=location,
            birth_time=birth_datetime
        )
        
        session.add(db_person)
        session.commit()
        
        return {"status": "success", "person_id": person_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/Calculate/DasaAtRange")
async def calculate_dasa_at_range(
    location: str,      # Birth location name
    birth_time: str,    # Format: "HH:MM DD/MM/YYYY +HH:MM" 
    start_time: str,    # Format: "HH:MM DD/MM/YYYY +HH:MM"
    end_time: str,      # Format: "HH:MM DD/MM/YYYY +HH:MM"
    start_location: str = None,  # Optional start time location
    end_location: str = None,    # Optional end time location  
    dasa_system: str = "Vimshottari",  # Supported: Vimshottari, Ashtottari
    ayanamsa: str = "Raman",  # Supported: Raman, Lahiri, KP
    levels: int = 3,    # Range: 1-7
):
    """Calculate dasa periods between start and end time for a person.
    
    Args:
        location: Birth location name
        birth_time: Birth date and time in format "HH:MM DD/MM/YYYY"
        start_time: Start date and time in format "HH:MM DD/MM/YYYY"
        end_time: End date and time in format "HH:MM DD/MM/YYYY"
    """
    try:
        # Parse locations into GeoLocation objects
        birth_lat, birth_lon = 0.0, 0.0  # Implement geocoding for birth location
        birth_location = GeoLocation(location, birth_lat, birth_lon)
        
        # Use birth location as default for start/end if not specified
        start_location = GeoLocation(start_location, *get_coords(start_location)) if start_location else birth_location
        end_location = GeoLocation(end_location, *get_coords(end_location)) if end_location else birth_location
        
        # Create Time objects with locations and timezone offsets
        birth = Time(birth_time, birth_location)
        start = Time(start_time, start_location) 
        end = Time(end_time, end_location)
        
        # Calculate dasas
        dasa_periods = Calculator.calculate_dasa_at_range(birth, start, end)
        
        return dasa_periods
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/Calculate/Tarabala")
async def calculate_tarabala(
    location: str,
    time: str,  # Format: "HH:MM DD/MM/YYYY" (e.g. "14:30 25/12/1990")
):
    """Calculate Tarabala (birth star auspiciousness) for given time and location.
    
    Args:
        location: Location name
        time: Date and time in format "HH:MM DD/MM/YYYY"
    """
    try:
        # Parse location into GeoLocation
        lat, lon = 0.0, 0.0  # Implement geocoding
        geo_location = GeoLocation(location, lat, lon)
        birth_time = Time(time, geo_location)
        
        # Calculate Tarabala
        tarabala = Calculator.calculate_tarabala(birth_time)
        
        return tarabala
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/Calculate/Horoscope")
async def calculate_horoscope(
    location: str,
    time: str,  # Format: "HH:MM DD/MM/YYYY" (e.g. "14:30 25/12/1990")
):
    """Calculate horoscope for given time and location.
    
    Args:
        location: Location name
        time: Date and time in format "HH:MM DD/MM/YYYY"
    """
    try:
        # Parse location into GeoLocation
        lat, lon = 0.0, 0.0  # Implement geocoding
        geo_location = GeoLocation(location, lat, lon)
        birth_time = Time(time, geo_location)
        
        # Calculate positions
        planet_positions = Calculator.calculate_planet_positions(birth_time)
        houses = Calculator.calculate_houses(birth_time)
        dasa = Calculator.calculate_dasa(birth_time)
        
        return {
            "planet_positions": planet_positions,
            "houses": houses,
            "dasa": dasa
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/Calculate/Events/{person_id}")
async def calculate_events(
    person_id: str,
    start_time: str,  # Format: "HH:MM DD/MM/YYYY" (e.g. "14:30 25/12/1990")
    end_time: str,    # Format: "HH:MM DD/MM/YYYY" (e.g. "14:30 26/12/1990")
):
    """Calculate events for a person between start and end times.
    
    Args:
        person_id: UUID of the person
        start_time: Start date and time in format "HH:MM DD/MM/YYYY"
        end_time: End date and time in format "HH:MM DD/MM/YYYY"
    """
    try:
        session = Session(engine)
        db_person = session.query(PersonDB).filter_by(id=person_id).first()
        
        if not db_person:
            raise HTTPException(status_code=404, detail="Person not found")
            
        # Convert DB person to domain model
        if not db_person.birth_time:
            raise HTTPException(status_code=400, detail="Birth time not set for this person")
            
        geo_location = GeoLocation(db_person.location_name, 
                                 db_person.latitude, 
                                 db_person.longitude)
        # Format birth time with correct format
        birth_time = Time(
            f"{db_person.birth_time.strftime('%H:%M/%d/%m/%Y')}",
            geo_location
        )
        person = Person(db_person.id, db_person.name, db_person.notes,
                       birth_time, db_person.gender, db_person.owner_id, [])
        
        # Parse and format start time
        start_parts = start_time.split()
        if len(start_parts) == 2:  # Format: "HH:MM DD/MM/YYYY"
            time_part, date_part = start_parts
            start_time = f"{time_part}/{date_part}"
        
        # Parse and format end time
        end_parts = end_time.split()
        if len(end_parts) == 2:  # Format: "HH:MM DD/MM/YYYY"
            time_part, date_part = end_parts
            end_time = f"{time_part}/{date_part}"
            
        start = Time(start_time, geo_location)
        end = Time(end_time, geo_location)
        events = Calculator.predict_events(person, start, end)
        
        return {"events": events}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
