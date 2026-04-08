from pydantic import BaseModel, Field
from typing import List


class UploadResponse(BaseModel):
    message: str = Field(..., example="PDF uploaded, embedded, and stored in FAISS successfully")
    filename: str = Field(..., example="123e4567_resume.pdf")
    original_filename: str = Field(..., example="resume.pdf")
    file_path: str = Field(..., example="data/uploads/123e4567_resume.pdf")
    total_characters: int = Field(..., example=2450)
    total_chunks: int = Field(..., example=6)
    stored_embeddings: int = Field(..., example=6)


class SourceChunk(BaseModel):
    rank: int = Field(..., example=1)
    chunk_id: int = Field(..., example=5)
    text: str = Field(..., example="This chunk discusses the main topic of the document.")
    distance: float = Field(..., example=1.38)


class ChatResponse(BaseModel):
    question: str = Field(..., example="What is this document about?")
    answer: str = Field(..., example="This document describes AI and backend projects, including a RAG chatbot and secure API systems.")
    sources: List[SourceChunk]