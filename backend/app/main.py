from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import documents

app = FastAPI(title="AI Document Management Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router, prefix="/documents", tags=["Documents"])

@app.get("/")
def root():
    return {"message": "AI Document Management Platform API is running"}