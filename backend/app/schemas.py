from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class DocumentResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    content_type: str
    extracted_text: Optional[str]
    summary: Optional[str]
    tags: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True