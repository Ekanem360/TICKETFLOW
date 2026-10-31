from pydantic import BaseModel
from datetime import datetime
class UserCreate(BaseModel):
    email: str
    password: str
    role: str = "customer"
class EventCreate(BaseModel):
    title: str
    description: str
    date: datetime
    venue: str