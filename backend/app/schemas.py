from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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