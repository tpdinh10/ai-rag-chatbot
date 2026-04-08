from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def get_embedding(text: str) -> list[float]:
    """
    Generate an embedding for one text string.
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Embedding input must be a non-empty string.")

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


def get_embeddings_for_chunks(chunks: list) -> list[dict]:
    """
    Generate embeddings for a list of chunks.
    Supports both:
    - list[str]
    - list[dict] where each dict has 'chunk_id' and 'content'
    """
    embedded_chunks = []
    MAX_CHARS = 2000

    for i, chunk in enumerate(chunks, start=1):
        if isinstance(chunk, dict):
            raw_text = chunk.get("content", "")
            chunk_id = chunk.get("chunk_id", i)
        else:
            raw_text = chunk
            chunk_id = i

        if not isinstance(raw_text, str):
            continue

        chunk_text = raw_text.strip()

        if not chunk_text:
            continue

        if len(chunk_text) > MAX_CHARS:
            chunk_text = chunk_text[:MAX_CHARS]

        try:
            embedding = get_embedding(chunk_text)
        except Exception as e:
            print(f"Skipping chunk {chunk_id} because embedding failed: {e}")
            continue

        embedded_chunks.append({
            "chunk_id": chunk_id,
            "text": chunk_text,
            "embedding": embedding
        })

    return embedded_chunks