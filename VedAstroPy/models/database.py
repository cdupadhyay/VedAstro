
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class PersonDB(Base):
    __tablename__ = 'persons'
    
    id = Column(String, primary_key=True)
    name = Column(String)
    birth_time = Column(DateTime)
    gender = Column(String)
    owner_id = Column(String)
    notes = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    location_name = Column(String)
    
    events = relationship("EventDB", back_populates="person")

class EventDB(Base):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True)
    person_id = Column(String, ForeignKey('persons.id'))
    event_type = Column(String)
    start_time = Column(DateTime)
    description = Column(String)
    
    person = relationship("PersonDB", back_populates="events")

# Create database engine
engine = create_engine('sqlite:///vedastro.db')
Base.metadata.create_all(engine)
