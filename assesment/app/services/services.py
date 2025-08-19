from sqlalchemy import select
from app.db.database import database
from app.repositories.repositories import (
    EventRepository,
    AttendeeRepository,
    RepositoryError,
)
from app.models.models import Event, Attendee
from app.models.schemas import EventCreate, AttendeeCreate
from datetime import datetime
import pytz  # or use zoneinfo for Python 3.9+

UTC = pytz.UTC
IST = pytz.timezone("Asia/Kolkata")


class EventService:
    def __init__(self, event_repo: EventRepository):
        self.event_repo = event_repo

    async def create_event(self, event_data: EventCreate) -> Event:
        """
        Create a new event. Converts start/end times to UTC before storing.
        Raises ValueError if creation fails.
        """
        try:
            data = event_data.dict()
            # Convert to UTC if not already
            for field in ["start_time", "end_time"]:
                dt = data[field]
                if dt.tzinfo is None:
                    dt = IST.localize(dt)
                data[field] = dt.astimezone(UTC)

            # Validation
            if not isinstance(data["max_capacity"], int):
                raise ValueError("Max capacity must be an integer")
            if data["max_capacity"] <= 0:
                raise ValueError("Max capacity must be greater than zero")
            if data["max_capacity"] >= 1000:
                raise ValueError("Max capacity cannot exceed 1000")
            if data["start_time"] >= data["end_time"]:
                raise ValueError("Start time must be before end time")

            # DB call
            return await self.event_repo.create_event(data)
        except RepositoryError as e:
            raise ValueError(str(e))

    async def get_upcoming_events(self, limit=10, offset=0):
        from datetime import datetime
        try:
            query = select(Event).where(Event.start_time >= datetime.now()).limit(limit).offset(offset)
            rows = await database.fetch_all(query)
            return [Event(**dict(row)) for row in rows]
        except Exception as e:
            raise RepositoryError(f"Database error during fetching events: {str(e)}")

    async def get_upcoming_events(self, limit=10, offset=0):
        """
        Get all upcoming events with pagination. Converts times to IST before returning.
        Raises ValueError if query fails.
        """
        try:
            events = await self.event_repo.get_upcoming_events(limit=limit, offset=offset)
            for event in events:
                event.start_time = event.start_time.astimezone(IST)
                event.end_time = event.end_time.astimezone(IST)
            return events
        except RepositoryError as e:
            raise ValueError(str(e))

    async def get_event(self, event_id: int):
        """
        Get a single event by ID. Converts times to IST before returning.
        Raises ValueError if not found.
        """
        try:
            event = await self.event_repo.get_event(event_id)
            event.start_time = event.start_time.astimezone(IST)
            event.end_time = event.end_time.astimezone(IST)
            return event
        except RepositoryError as e:
            raise ValueError(str(e))

    async def delete_event(self, event_id: int):
        """
        Delete an event by ID. Raises ValueError if not found or delete fails.
        """
        try:
            return await self.event_repo.delete_event(event_id)
        except RepositoryError as e:
            raise ValueError(str(e))


class AttendeeService:
    def __init__(self, attendee_repo: AttendeeRepository, event_repo: EventRepository):
        self.attendee_repo = attendee_repo
        self.event_repo = event_repo

    async def register_attendee(self, event_id: int, attendee_data: AttendeeCreate):
        """
        Register an attendee for an event. Raises ValueError for business or DB errors.
        """
        try:
            event = await self.event_repo.get_event(event_id)
            if not event:
                raise ValueError("Event not found")
            count = await self.attendee_repo.attendee_count(event_id)
            if count >= event.max_capacity:
                raise ValueError("Event is full")
            duplicate = await self.attendee_repo.is_duplicate_registration(
                event_id, attendee_data.email
            )
            if duplicate:
                raise ValueError("Duplicate registration")
            attendee_dict = attendee_data.dict()
            attendee_dict["event_id"] = event_id
            return await self.attendee_repo.register_attendee(attendee_dict)
        except RepositoryError as e:
            raise ValueError(str(e))

    async def get_attendees_for_event(self, event_id: int):
        """
        Get all attendees for an event. Raises ValueError if query fails.
        """
        try:
            return await self.attendee_repo.get_attendees_for_event(event_id)
        except RepositoryError as e:
            raise ValueError(str(e))
