from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
from uuid import uuid4

from app.services.pdf_loader import extract_text_from_pdf
from app.services.text_splitter import split_text_into_chunks
from app.services.embedding_service import get_embeddings_for_chunks
from app.services.vector_store import save_to_faiss
from app.models.response_models import UploadResponse

router = APIRouter()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    unique_filename = f"{uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        extracted_text = extract_text_from_pdf(file_path)
        chunks = split_text_into_chunks(extracted_text)
        embedded_chunks = get_embeddings_for_chunks(chunks)
        save_to_faiss(embedded_chunks)

        return {
            "message": "PDF uploaded, embedded, and stored in FAISS successfully",
            "filename": unique_filename,
            "original_filename": file.filename,
            "file_path": file_path,
            "total_characters": len(extracted_text),
            "total_chunks": len(chunks),
            "stored_embeddings": len(embedded_chunks)
        }

    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")