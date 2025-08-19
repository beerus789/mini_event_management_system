from fastapi import APIRouter, HTTPException
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
from app.db.database import database

router = APIRouter()

@router.on_event("startup")
async def startup():
    await database.connect()

@router.on_event("shutdown")
async def shutdown():
    await database.disconnect()




@router.post("/events", response_model=EventOut)
async def create_event(event: EventCreate):
    """
    Create a new event.
    This endpoint allows users to create a new event by providing the necessary details.
    Returns 400 if creation fails.
    """
    event_service = EventService(EventRepository())
    try:
        return await event_service.create_event(event)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/events", response_model=List[EventOut])
async def list_events(limit: int = 10, offset: int = 0):
    event_service = EventService(EventRepository())
    try:
        return await event_service.get_upcoming_events(limit=limit, offset=offset)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# @router.get("/events", response_model=List[EventOut])
# async def list_events():
#     """
#     List all upcoming events.
#     This endpoint retrieves a list of all upcoming events.
#     Returns 400 if query fails.
#     """
#     event_service = EventService(EventRepository())
#     try:
#         return await event_service.get_upcoming_events()
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))


@router.delete("/events/{event_id}", response_model=EventOut)
async def delete_event(event_id: int):
    """
    Delete an event by its ID.
    Returns 404 if not found or delete fails.
    """
    event_service = EventService(EventRepository())
    try:
        return await event_service.delete_event(event_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/events/{event_id}/register", response_model=AttendeeOut)
async def register_attendee(event_id: int, attendee: AttendeeCreate):
    """
    Register an attendee for a specific event.
    Prevents overbooking and duplicate registrations.
    Returns 400 if registration fails.
    """
    attendee_service = AttendeeService(AttendeeRepository(), EventRepository())
    try:
        return await attendee_service.register_attendee(event_id, attendee)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/events/{event_id}/attendees", response_model=AttendeeListOut)
async def get_attendees(event_id: int):
    """
    Get all registered attendees for an event.
    Returns 400 if query fails.
    """
    attendee_service = AttendeeService(AttendeeRepository(), EventRepository())
    try:
        attendees = await attendee_service.get_attendees_for_event(event_id)
        return {"attendees": attendees}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
