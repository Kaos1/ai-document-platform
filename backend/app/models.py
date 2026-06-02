from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    documents = relationship("Document", back_populates="owner")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    extracted_text = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)
    embedding = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    owner = relationship("User", back_populates="documents")