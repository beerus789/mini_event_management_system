from app.repositories.repositories import EventRepository, AttendeeRepository
from app.models.models import Event, Attendee
from app.models.schemas import EventCreate, AttendeeCreate
from sqlalchemy.orm import Session

class EventService:
    def __init__(self, event_repo: EventRepository):
        self.event_repo = event_repo

    def create_event(self, event_data: EventCreate) -> Event:
        event = Event(**event_data.dict())
        return self.event_repo.create_event(event)

    def get_upcoming_events(self):
        return self.event_repo.get_upcoming_events()

    def get_event(self, event_id: int):
        return self.event_repo.get_event(event_id)
    
    def delete_event(self, event_id: int):
        event = self.event_repo.get_event(event_id)
        if not event:
            raise ValueError("Event not found")
        return self.event_repo.delete_event(event_id)

class AttendeeService:
    def __init__(self, attendee_repo: AttendeeRepository, event_repo: EventRepository):
        self.attendee_repo = attendee_repo
        self.event_repo = event_repo

    def register_attendee(self, event_id: int, attendee_data: AttendeeCreate):
        event = self.event_repo.get_event(event_id)
        if not event:
            raise ValueError("Event not found")
        if self.attendee_repo.attendee_count(event_id) >= event.max_capacity:
            raise ValueError("Event is full")
        if self.attendee_repo.is_duplicate_registration(event_id, attendee_data.email):
            raise ValueError("Duplicate registration")
        attendee = Attendee(**attendee_data.dict(), event_id=event_id)
        return self.attendee_repo.register_attendee(attendee)

    def get_attendees_for_event(self, event_id: int):
        return self.attendee_repo.get_attendees_for_event(event_id)
