from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.schemas import (
    EventCreate,
    EventOut,
    AttendeeCreate,
    AttendeeOut,
    AttendeeListOut,
)
from app.repositories.repositories import EventRepository, AttendeeRepository
from app.services.services import EventService, AttendeeService
from typing import List

router = APIRouter()


def get_db():
    """Dependency to get the database session."""
    """This function provides a database session for each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/events", response_model=EventOut)
async def create_event(event: EventCreate, db: Session = Depends(get_db)):
    """
    Create a new event.
    This endpoint allows users to create a new event by providing the necessary details.
    """
    event_service = EventService(EventRepository(db))
    return event_service.create_event(event)


@router.get("/events", response_model=List[EventOut])
async def list_events(db: Session = Depends(get_db)):
    """
    List all upcoming events.
    This endpoint retrieves a list of all upcoming events.
    """
    event_service = EventService(EventRepository(db))
    return event_service.get_upcoming_events()


@router.delete("/events/{event_id}", response_model=EventOut)
async def delete_event(event_id: int, db: Session = Depends(get_db)):
    """
    Delete an event by its ID.
    """
    event_service = EventService(EventRepository(db))
    return event_service.delete_event(event_id)


@router.post("/events/{event_id}/register", response_model=AttendeeOut)
async def register_attendee(
    event_id: int, attendee: AttendeeCreate, db: Session = Depends(get_db)
):
    """
    Register an attendee for a specific event.
    Prevents overbooking and duplicate registrations.
    """
    attendee_service = AttendeeService(AttendeeRepository(db), EventRepository(db))
    try:
        return attendee_service.register_attendee(event_id, attendee)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/events/{event_id}/attendees", response_model=AttendeeListOut)
async def get_attendees(event_id: int, db: Session = Depends(get_db)):
    """
    Get all registered attendees for an event.
    """
    attendee_service = AttendeeService(AttendeeRepository(db), EventRepository(db))
    attendees = attendee_service.get_attendees_for_event(event_id)
    return {"attendees": attendees}
