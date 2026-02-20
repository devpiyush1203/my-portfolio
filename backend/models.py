from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
import uuid

class ContactMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    message: str
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "pending"

class ContactMessageCreate(BaseModel):
    name: str
    email: EmailStr
    message: str

class ResumeMetadata(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    original_name: str
    mime_type: str
    size: int
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    file_path: str
    is_active: bool = True

class ContactResponse(BaseModel):
    success: bool
    message: str