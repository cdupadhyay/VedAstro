from fastapi import FastAPI, HTTPException
import json
from sqlalchemy.orm import Session
from datetime import datetime
from models.base import Person, Time, GeoLocation
from models.database import PersonDB, EventDB, engine
from core.calculator import Calculator
from typing import List, Dict
import uuid
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

app = FastAPI()

def get_coords(location: str) -> tuple[float, float]:
    """Convert location name to coordinates using geocoding"""
    try:
        geolocator = Nominatim(user_agent="vedastro_geocoder")
        location_data = geolocator.geocode(location, timeout=10)
        if location_data:
            return (location_data.latitude, location_data.longitude)
        return None  # Return None if location not found
    except (GeocoderTimedOut, GeocoderUnavailable):
        return None  # Return None on geocoding error

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
        lat, lon = get_coords(location)

        time_str = f"{birth_time} {birth_date}"  # Format: "HH:MM DD/MM/YYYY"
        birth_datetime = datetime.strptime(time_str, "%H:%M %d/%m/%Y")

        session = Session(engine)

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
    location: str,
    birth_time: str, 
    start_time: str,
    end_time: str,
    start_location: str = None,
    end_location: str = None,
    dasa_system: str = "Vimshottari",
    ayanamsa: str = "Raman",
    levels: int = 3,
    precision_hours: int = 504  # Match C# default
):
    print(f"DEBUG: Received parameters:")
    print(f"location: {location}")
    print(f"birth_time: {birth_time}")
    print(f"start_time: {start_time}")
    print(f"end_time: {end_time}")
    """Calculate dasa periods between start and end time for a person.

    Args:
        location: Birth location name in any of these formats:
                 - City only: "London"
                 - City, Country: "Paris, France"
                 - City, State, Country: "Ajmer, Rajasthan, India"
                 - City with state/province: "New Delhi, India"
        birth_time: Birth date and time with UTC offset in format "HH:MM/DD/MM/YYYY/±HH:MM" (e.g. "14:30/25/12/1990/+05:30")
        start_time: Start date and time with UTC offset in format "HH:MM/DD/MM/YYYY/±HH:MM" (e.g. "14:30/25/12/1990/+05:30") 
        end_time: End date and time with UTC offset in format "HH:MM/DD/MM/YYYY/±HH:MM" (e.g. "14:30/25/12/2024/+05:30")
        start_location: Optional location for start time, uses same format as birth location
        end_location: Optional location for end time, uses same format as birth location
        dasa_system: Dasa system to use, either "Vimshottari" or "Ashtottari"
        ayanamsa: Ayanamsa to use, one of "Raman", "Lahiri", or "KP"
        levels: Number of dasa levels to calculate (1-7)

    Returns:
        Dictionary containing dasa periods or error message if location not found
    """
    try:
        try:
            print("DEBUG: Getting birth coordinates")
            # Get birth location coordinates
            birth_coords = get_coords(location)
            if birth_coords is None:
                return {"error": f"Location not found: {location}"}
            birth_lat, birth_lon = birth_coords
            print(f"DEBUG: Birth coordinates found: lat={birth_lat}, lon={birth_lon}")
            birth_location = GeoLocation(location, birth_lat, birth_lon)
        except Exception as e:
            print(f"DEBUG: Error getting coordinates: {str(e)}")
            raise

        # Handle start location
        if start_location:
            start_coords = get_coords(start_location)
            if start_coords is None:
                return {"error": f"Start location not found: {start_location}"}
            start_location = GeoLocation(start_location, *start_coords)
        else:
            start_location = birth_location

        # Handle end location
        if end_location:
            end_coords = get_coords(end_location)
            if end_coords is None:
                return {"error": f"End location not found: {end_location}"}
            end_location = GeoLocation(end_location, *end_coords) 
        else:
            end_location = birth_location

        # Validate time format
        def validate_time_format(time_str):
            try:
                # Convert old format (spaces and dots) to new format (slashes)
                # Example: "14:43 17/02/1977 +05.30" -> "14:43/17/02/1977/+05:30"
                time_str = time_str.replace(' ', '/').replace('.', ':')

                # Convert UTC offset format from +HH:MM to +HH:MM
                if " +" in time_str or " -" in time_str:
                    time_parts = time_str.rsplit(" ", 1)
                    base_time = time_parts[0].replace(" ", "/")
                    offset = time_parts[1]
                    time_str = f"{base_time}/{offset}"

                # Check if format matches HH:MM/DD/MM/YYYY/±HH:MM
                time_parts = time_str.split('/')

                # Handle case where only time is provided
                if len(time_parts) == 1 and ':' in time_str:
                    # Default to current date and +00:00 timezone
                    from datetime import datetime
                    now = datetime.now()
                    time_str = f"{time_str}/{now.day:02d}/{now.month:02d}/{now.year}/+00:00"
                    time_parts = time_str.split('/')

                if len(time_parts) != 5:
                    return {"error": f"Invalid time format: {time_str}. Expected format: HH:MM/DD/MM/YYYY/±HH:MM"}

                time, day, month, year, offset = time_parts
                if not (offset.startswith('+') or offset.startswith('-')):
                    return {"error": f"Invalid UTC offset format in {time_str}. Must start with + or -"}

                return None
            except Exception as e:
                return {"error": f"Invalid time format: {str(e)}"}

        # Validate all time inputs
        for time_str, desc in [(birth_time, "birth time"), (start_time, "start time"), (end_time, "end time")]:
            print(f"DEBUG: Validating {desc}: {time_str}")
            error = validate_time_format(time_str)
            if error:
                print(f"DEBUG: Time validation error for {desc}: {error}")
                return error
            print(f"DEBUG: {desc} validated successfully")

        birth = Time(birth_time, birth_location)
        start = Time(start_time, start_location) 
        end = Time(end_time, end_location)

        dasa_periods = Calculator.calculate_dasa_at_range(birth, start, end, precision_hours=precision_hours)

        # Print first dasa period for debugging
        print("\nPython Output First Dasa:")
        print(json.dumps(list(dasa_periods["Payload"].values())[0], indent=2))

        return dasa_periods
    except Exception as e:
        print(f"ERROR: {str(e)}")
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
        lat, lon = get_coords(location)
        geo_location = GeoLocation(location, lat, lon)
        birth_time = Time(time, geo_location)

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
        lat, lon = get_coords(location)
        geo_location = GeoLocation(location, lat, lon)
        birth_time = Time(time, geo_location)

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

        if not db_person.birth_time:
            raise HTTPException(status_code=400, detail="Birth time not set for this person")

        geo_location = GeoLocation(db_person.location_name, 
                                 db_person.latitude, 
                                 db_person.longitude)
        birth_time = Time(
            f"{db_person.birth_time.strftime('%H:%M/%d/%m/%Y')}",
            geo_location
        )
        person = Person(db_person.id, db_person.name, db_person.notes,
                       birth_time, db_person.gender, db_person.owner_id, [])

        start_parts = start_time.split()
        if len(start_parts) == 2:  # Format: "HH:MM DD/MM/YYYY"
            time_part, date_part = start_parts
            start_time = f"{time_part}/{date_part}"

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