# 🧠 AI Chatbot with RAG (Retrieval-Augmented Generation)

Build a backend AI system that answers questions based on uploaded documents using **Retrieval-Augmented Generation (RAG)**.

Instead of relying only on pre-trained knowledge, the system retrieves relevant document content **using vector search and generates grounded responses, reducing hallucination**.

---
## 🌐 Live Demo
API: https://ai-rag-chatbot-odu3.onrender.com
Swagger UI: https://ai-rag-chatbot-odu3.onrender.com/docs
Health Check: https://ai-rag-chatbot-odu3.onrender.com/health

👉 Live demo available — try it directly in your browser

## 🚀 Features

- 📄 Upload PDF documents  
- 🔍 Extract and process document text  
- ✂️ Paragraph-based chunking for better context  
- 🧠 Generate embeddings using OpenAI API  
- ⚡ Store and search vectors using FAISS  
- 💬 Ask questions and get grounded AI answers  
- 📚 Return source chunks for transparency
- 🌐 Deployed backend API (Render)  

---

## 🧠 How It Works (RAG Pipeline)

1. **Document Ingestion**  
   Upload a PDF file

2. **Text Extraction**  
   Extract raw text using `pypdf`

3. **Chunking**  
   Split text into paragraph-based chunks

4. **Embedding Generation**  
   Convert chunks into vector embeddings

5. **Vector Storage**  
   Store embeddings in FAISS

6. **Query Processing**  
   Convert user question into embedding

7. **Similarity Search**  
   Retrieve most relevant chunks

8. **Response Generation**  
   Generate final answer using retrieved context + LLM

---

## 🛠️ Tech Stack

- **Backend:** FastAPI (Python)
- **AI / LLM:** OpenAI API
- **Vector Database:** FAISS
- **PDF Processing:** pypdf
- **Data Handling:** NumPy

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/tpdinh10/ai-rag-chatbot.git
cd ai-rag-chatbot
```
### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Set environment variables

Create a `.env` file:
```env

OPENAI_API_KEY=your_openai_api_key_here
```
### 5. Run the server
```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

http://127.0.0.1:8000/docs

## 📡 API Endpoints
### 📄 Upload Document

POST `/upload`

Upload a PDF and process it into vector storage.

### 💬 Chat with Document

POST `/chat`

Request:
```JSON
{
  "question": "What is this document about?",
  "top_k": 3
}
```
Response:
```JSON
{
  "question": "What is this document about?",
  "answer": "This document describes AI and backend systems...",
  "sources": [
    {
      "rank": 1,
      "chunk_id": 3,
      "text": "...",
      "distance": 0.81
    }
  ]
}
```
## 🧪 Example Use Cases
- Document question answering
- Resume analysis
- Knowledge base chatbot
- Customer support assistant
## ⚠️ Known Limitations
- Retrieval quality depends on chunking strategy
- FAISS index resets on each upload (single-document mode)
- Large PDFs may require chunking optimization
## 🔮 Future Improvements
- Multi-document support
- Metadata filtering (file name, section)
- Frontend UI (React or web app)
- Deployment (Render / AWS)
- Streaming responses
