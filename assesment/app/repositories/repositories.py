from app.db.database import SessionLocal
from app.models.models import Event, Attendee
from sqlalchemy.orm import Session
from sqlalchemy import and_

class EventRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_event(self, event: Event) -> Event:
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def get_upcoming_events(self):
        from datetime import datetime
        # return self.db.query(Event).filter(Event.start_time >= datetime.now()).all()
        return self.db.query(Event).all()

    def get_event(self, event_id: int):
        return self.db.query(Event).filter(Event.id == event_id).first()

    def delete_event(self, event_id: int):
        event = self.get_event(event_id)
        if event:
            self.db.delete(event)
            self.db.commit()
            return event
        return None

class AttendeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def register_attendee(self, attendee: Attendee) -> Attendee:
        self.db.add(attendee)
        self.db.commit()
        self.db.refresh(attendee)
        return attendee

    def get_attendees_for_event(self, event_id: int):
        return self.db.query(Attendee).filter(Attendee.event_id == event_id).all()

    def is_duplicate_registration(self, event_id: int, email: str) -> bool:
        return self.db.query(Attendee).filter(and_(Attendee.event_id == event_id, Attendee.email == email)).first() is not None

    def attendee_count(self, event_id: int) -> int:
        return self.db.query(Attendee).filter(Attendee.event_id == event_id).count()
