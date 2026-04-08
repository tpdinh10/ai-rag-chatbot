from fastapi import APIRouter, HTTPException

from app.models.request_models import QuestionRequest
from app.models.response_models import ChatResponse
from app.services.embedding_service import get_embedding
from app.services.vector_store import search_similar_chunks
from app.services.rag_service import generate_rag_answer

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_with_document(request: QuestionRequest):
    try:
        query_embedding = get_embedding(request.question)
        retrieved_chunks = search_similar_chunks(query_embedding, request.top_k)
        answer = generate_rag_answer(request.question, retrieved_chunks)

        return {
            "question": request.question,
            "answer": answer,
            "sources": retrieved_chunks
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")