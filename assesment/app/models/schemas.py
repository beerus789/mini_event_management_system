from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List

class EventCreate(BaseModel):
    name: str
    location: str
    start_time: datetime
    end_time: datetime
    max_capacity: int

class EventOut(BaseModel):
    id: int
    name: str
    location: str
    start_time: datetime
    end_time: datetime
    max_capacity: int

    class Config:
        from_attributes = True


class AttendeeCreate(BaseModel):
    name: str
    email: EmailStr

class AttendeeOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    class Config:
        from_attributes = True

class AttendeeListOut(BaseModel):
    attendees: List[AttendeeOut]
