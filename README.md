# AI Document Management Platform

A full-stack document management platform that allows users to upload, process, search, and manage PDF and image documents. The application uses OCR for text extraction, automatic summaries and tags, semantic search with embeddings, JWT authentication, and Dockerized deployment.

## Features

- User registration and login with JWT authentication
- User-specific document storage and access control
- Upload PDF, PNG, JPG, and JPEG files
- Extract text from uploaded documents using OCR
- Generate automatic document summaries and keyword tags
- Search documents by exact keywords
- Search documents semantically using SentenceTransformers embeddings
- Download and delete uploaded documents
- React frontend with FastAPI backend
- PostgreSQL database
- Docker Compose setup for frontend, backend, and database

## Tech Stack

**Frontend**
- React
- Vite
- JavaScript
- Axios
- CSS

**Backend**
- FastAPI
- Python
- SQLAlchemy
- JWT authentication
- Pydantic
- Tesseract OCR
- SentenceTransformers

**Database**
- PostgreSQL

**DevOps**
- Docker
- Docker Compose

## AI Features

The project uses AI/document intelligence in several ways:

1. **OCR text extraction**  
   Uploaded images and PDFs are processed to extract readable text.

2. **Semantic search**  
   Document text is converted into embeddings using SentenceTransformers. Search queries are also embedded, then compared with document embeddings using cosine similarity to retrieve documents by meaning.

3. **Automatic summaries and tags**  
   Extracted text is processed to generate short summaries and keyword tags for easier document browsing.

## Architecture

```txt
React Frontend
      |
      v
FastAPI Backend
      |
      v
PostgreSQL Database

Document Upload Flow:
User uploads file
→ Backend validates and stores file
→ OCR extracts text
→ Summary, tags, and embeddings are generated
→ Metadata is stored in PostgreSQL
→ User can search by keyword or semantic meaning