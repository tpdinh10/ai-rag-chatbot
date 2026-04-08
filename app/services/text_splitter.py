import re


def split_text_into_chunks(text: str, chunk_size: int = 1000) -> list[dict]:
    """
    Split text by paragraphs/sections instead of raw character slicing.
    This keeps related content together better for RAG.
    """
    if not text or not text.strip():
        return []

    # Normalize line breaks
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Split by blank lines first
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]

    chunks = []
    current_chunk = ""
    chunk_id = 1

    for para in paragraphs:
        # If adding this paragraph stays within limit, keep building current chunk
        if len(current_chunk) + len(para) + 2 <= chunk_size:
            if current_chunk:
                current_chunk += "\n\n" + para
            else:
                current_chunk = para
        else:
            # Save current chunk if it exists
            if current_chunk:
                chunks.append({
                    "chunk_id": chunk_id,
                    "content": current_chunk
                })
                chunk_id += 1

            # If one paragraph alone is too big, split it safely
            if len(para) > chunk_size:
                start = 0
                while start < len(para):
                    part = para[start:start + chunk_size].strip()
                    if part:
                        chunks.append({
                            "chunk_id": chunk_id,
                            "content": part
                        })
                        chunk_id += 1
                    start += chunk_size
                current_chunk = ""
            else:
                current_chunk = para

    # Add final chunk
    if current_chunk:
        chunks.append({
            "chunk_id": chunk_id,
            "content": current_chunk
        })

    return chunks