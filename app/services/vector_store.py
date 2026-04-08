import os
import json
import faiss
import numpy as np

INDEX_DIR = "data/faiss_index"
INDEX_FILE = os.path.join(INDEX_DIR, "index.faiss")
METADATA_FILE = os.path.join(INDEX_DIR, "metadata.json")

os.makedirs(INDEX_DIR, exist_ok=True)


def save_to_faiss(embedded_chunks: list[dict]) -> None:
    """
    Save embedded chunks into FAISS index and metadata file.
    """
    if not embedded_chunks:
        raise ValueError("No embedded chunks to save.")

    embeddings = np.array(
        [chunk["embedding"] for chunk in embedded_chunks],
        dtype=np.float32
    )

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    faiss.write_index(index, INDEX_FILE)

    metadata = [
        {
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"]
        }
        for chunk in embedded_chunks
    ]

    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)


def load_faiss_index():
    """
    Load FAISS index and metadata.
    """
    if not os.path.exists(INDEX_FILE) or not os.path.exists(METADATA_FILE):
        raise FileNotFoundError("FAISS index or metadata file not found.")

    index = faiss.read_index(INDEX_FILE)

    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    return index, metadata


def search_similar_chunks(query_embedding: list[float], top_k: int = 3) -> list[dict]:
    """
    Search the most similar chunks from FAISS using the query embedding.
    """
    index, metadata = load_faiss_index()

    query_vector = np.array([query_embedding], dtype=np.float32)
    distances, indices = index.search(query_vector, top_k)

    results = []
    for rank, idx in enumerate(indices[0]):
        if idx < len(metadata):
            results.append({
                "rank": rank + 1,
                "chunk_id": metadata[idx]["chunk_id"],
                "text": metadata[idx]["text"],
                "distance": float(distances[0][rank])
            })

    return results