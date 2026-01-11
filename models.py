from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class LeadStatus(str, Enum):
    new = "new"
    contacted = "contacted"
    meeting = "meeting"
    client = "client"
    lost = "lost"


class LeadStatusUpdate(BaseModel):
    status: LeadStatus


class Lead(BaseModel):
    name: str
    email: str
    status: LeadStatus
    created_at: datetime | None = None


class UserRole(str, Enum):
    admin = "admin"
    salesperson = "handlowiec"


class User(BaseModel):
    username: str
    email: str
    password: str
    role: UserRole
