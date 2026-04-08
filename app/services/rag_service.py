from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_rag_answer(question: str, retrieved_chunks: list[dict]) -> str:
    """
    Generate a final answer using the user question and retrieved document chunks.
    """
    if not retrieved_chunks:
        return "I could not find relevant information in the document."

    context = "\n\n".join(
        [f"Chunk {chunk['chunk_id']}: {chunk['text']}" for chunk in retrieved_chunks]
    )

    prompt = f"""
You are a helpful AI assistant.
Answer the user's question using only the provided document context.
If the answer is not in the context, say that the information is not available in the document.

Document Context:
{context}

User Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You answer questions only from the provided document context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()