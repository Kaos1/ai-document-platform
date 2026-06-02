import os
import shutil
from uuid import uuid4
from typing import List

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Document
from app.schemas import DocumentResponse

from app.services.text_extraction import extract_text

from app.services.ai_processing import generate_summary, generate_tags, generate_embedding, rank_documents_by_similarity

from app.auth import get_current_user
from app.models import Document, User

router = APIRouter()

UPLOAD_DIR = "app/uploads"

ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/jpg"
}

@router.post("/upload", response_model=DocumentResponse)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, PNG, JPG, and JPEG files are allowed."
        )

    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text(file_path, file.content_type)
    summary = generate_summary(extracted_text)
    tags = generate_tags(extracted_text)
    embedding = generate_embedding(extracted_text)

    document = Document(
        filename=unique_filename,
        original_filename=file.filename,
        content_type=file.content_type,
        file_path=file_path,
        extracted_text=extracted_text,
        summary=summary,
        tags=tags,
        embedding=embedding,
        user_id=current_user.id
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


@router.get("/", response_model=List[DocumentResponse])
def get_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return (
        db.query(Document)
        .filter(Document.user_id == current_user.id)
        .order_by(Document.created_at.desc())
        .all()
    )

@router.get("/search/", response_model=List[DocumentResponse])
def search_documents(
    query: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return (
        db.query(Document)
        .filter(Document.user_id == current_user.id)
        .filter(Document.extracted_text.ilike(f"%{query}%"))
        .order_by(Document.created_at.desc())
        .all()
    )

@router.get("/semantic-search/", response_model=List[DocumentResponse])
def semantic_search_documents(
    query: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    documents = (
        db.query(Document)
        .filter(Document.user_id == current_user.id)
        .all()
    )

    ranked_documents = rank_documents_by_similarity(query, documents)

    return [document for document, score in ranked_documents[:5]]

@router.get("/{document_id}/download")
def download_document(document_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    document = (db.query(Document).filter(Document.id == document_id).filter(Document.user_id == current_user.id).first())

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if not os.path.exists(document.file_path):
        raise HTTPException(status_code=404, detail="File not found on server")

    return FileResponse(
        path=document.file_path,
        filename=document.original_filename,
        media_type=document.content_type
    )


@router.delete("/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    document = (db.query(Document).filter(Document.id == document_id).filter(Document.user_id == current_user.id).first())

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if os.path.exists(document.file_path):
        os.remove(document.file_path)

    db.delete(document)
    db.commit()

    return {"message": "Document deleted successfully"}