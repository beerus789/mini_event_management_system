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
        orm_mode = True
    
    # Add custom serializer for datetime fields
    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        data['start_time'] = self.start_time.strftime('%Y-%m-%d %H:%M')
        data['end_time'] = self.end_time.strftime('%Y-%m-%d %H:%M')
        return data

class AttendeeCreate(BaseModel):
    name: str
    email: EmailStr

class AttendeeOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    class Config:
        orm_mode = True

class AttendeeListOut(BaseModel):
    attendees: List[AttendeeOut]
