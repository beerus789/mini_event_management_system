from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    max_capacity = Column(Integer, nullable=False)
    attendees = relationship("Attendee", back_populates="event")

class Attendee(Base):
    __tablename__ = "attendees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    event = relationship("Event", back_populates="attendees")
