from pydantic import BaseModel, EmailStr
from uuid import uuid4
from datetime import datetime

class User(BaseModel):
    user_id: str = str(uuid4())
    user_name: str
    user_email: EmailStr
    mobile_number: str
    password: str
    created_on: datetime = datetime.utcnow()
    last_update: datetime = datetime.utcnow()

class Note(BaseModel):
    note_id: str = str(uuid4())
    note_title: str
    note_content: str
    created_on: datetime = datetime.utcnow()
    last_update: datetime = datetime.utcnow()