from fastapi import FastAPI
from app.routes.upload import router as upload_router
from app.routes.chat import router as chat_router

app = FastAPI(title="AI Chatbot with RAG")

app.include_router(upload_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {"message": "AI RAG Chatbot API is running"}