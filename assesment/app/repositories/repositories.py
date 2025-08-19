from app.db.database import database
from app.models.models import Event, Attendee
from sqlalchemy import select, insert, and_, func

class RepositoryError(Exception):
    """Custom exception for repository errors."""
    pass

class EventRepository:
    async def create_event(self, event_data: dict):
        """
        Create a new event in the database.
        Raises RepositoryError if creation fails.
        """
        try:
            query = insert(Event).values(**event_data)
            event_id = await database.execute(query)
            event = await self.get_event(event_id)
            if not event:
                raise RepositoryError("Event creation failed")
            return event
        except Exception as e:
            raise RepositoryError(f"Database error during event creation: {str(e)}")

    async def get_upcoming_events(self, limit=10, offset=0):
        """
        Fetch all upcoming events from the database with pagination.
        Raises RepositoryError if query fails.
        """
        from datetime import datetime
        try:
            query = select(Event).where(Event.start_time >= datetime.now()).limit(limit).offset(offset)
            rows = await database.fetch_all(query)
            return [Event(**dict(row)) for row in rows]
        except Exception as e:
            raise RepositoryError(f"Database error during fetching events: {str(e)}")

    async def get_event(self, event_id: int):
        """
        Fetch a single event by ID.
        Raises RepositoryError if not found or query fails.
        """
        try:
            query = select(Event).where(Event.id == event_id)
            row = await database.fetch_one(query)
            if not row:
                raise RepositoryError(f"Event with id {event_id} not found")
            return Event(**dict(row))
        except Exception as e:
            raise RepositoryError(f"Database error during fetching event: {str(e)}")

    async def delete_event(self, event_id: int):
        """
        Delete an event by ID.
        Raises RepositoryError if not found or query fails.
        """
        try:
            event = await self.get_event(event_id)
            from sqlalchemy import delete
            query = delete(Event).where(Event.id == event_id)
            await database.execute(query)
            return event
        except Exception as e:
            raise RepositoryError(f"Database error during deleting event: {str(e)}")

class AttendeeRepository:
    async def register_attendee(self, attendee_data: dict) -> Attendee:
        """
        Register a new attendee for an event.
        Raises RepositoryError if registration fails.
        """
        try:
            query = insert(Attendee).values(**attendee_data)
            attendee_id = await database.execute(query)
            attendee = await self.get_attendee(attendee_id)
            if not attendee:
                raise RepositoryError("Attendee registration failed")
            return attendee
        except Exception as e:
            raise RepositoryError(f"Database error during attendee registration: {str(e)}")

    async def get_attendee(self, attendee_id: int):
        """
        Fetch a single attendee by ID.
        Raises RepositoryError if not found or query fails.
        """
        try:
            query = select(Attendee).where(Attendee.id == attendee_id)
            row = await database.fetch_one(query)
            if not row:
                raise RepositoryError(f"Attendee with id {attendee_id} not found")
            return Attendee(**dict(row))
        except Exception as e:
            raise RepositoryError(f"Database error during fetching attendee: {str(e)}")

    async def get_attendees_for_event(self, event_id: int):
        """
        Fetch all attendees for a given event.
        Raises RepositoryError if query fails.
        """
        try:
            query = select(Attendee).where(Attendee.event_id == event_id)
            rows = await database.fetch_all(query)
            return [Attendee(**dict(row)) for row in rows]
        except Exception as e:
            raise RepositoryError(f"Database error during fetching attendees: {str(e)}")

    async def is_duplicate_registration(self, event_id: int, email: str) -> bool:
        """
        Check if an attendee with the given email is already registered for the event.
        Raises RepositoryError if query fails.
        """
        try:
            query = select(Attendee).where(and_(Attendee.event_id == event_id, Attendee.email == email))
            row = await database.fetch_one(query)
            return row is not None
        except Exception as e:
            raise RepositoryError(f"Database error during duplicate check: {str(e)}")

    async def attendee_count(self, event_id: int) -> int:
        """
        Get the number of attendees registered for an event.
        Raises RepositoryError if query fails.
        """
        try:
            query = select(func.count()).where(Attendee.event_id == event_id)
            result = await database.fetch_one(query)
            # result is a Row object, get the first value
            return list(result.values())[0] if result else 0
        except Exception as e:
            raise RepositoryError(f"Database error during attendee count: {str(e)}")
