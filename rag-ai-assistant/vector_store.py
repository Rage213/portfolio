import json
import os
import numpy as np
from typing import List, Dict, Tuple

class LocalVectorStore:
    """
    A lightweight, pure-python local Vector Store using NumPy 
    for cosine similarity matching. Persists index as a JSON file.
    """
    def __init__(self):
        self.chunks: List[str] = []
        self.vectors: List[np.ndarray] = []
        self.metadata: List[Dict[str, any]] = []

    def add_documents(self, chunks: List[str], vectors: List[List[float]], metadata: List[Dict[str, any]] = None):
        """Adds text chunks and their respective vectors to the database."""
        for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
            self.chunks.append(chunk)
            self.vectors.append(np.array(vector, dtype=np.float32))
            
            meta = metadata[i] if metadata and i < len(metadata) else {}
            self.metadata.append(meta)

    def cosine_similarity(self, v1: np.ndarray, v2: np.ndarray) -> float:
        """Calculates cosine similarity between two vectors."""
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        if norm_v1 == 0 or norm_v2 == 0:
            return 0.0
        return float(np.dot(v1, v2) / (norm_v1 * norm_v2))

    def search(self, query_vector: List[float], top_k: int = 3) -> List[Dict[str, any]]:
        """
        Searches for top_k most similar chunks to the query vector.
        Returns list of matches with contents, similarity score, and metadata.
        """
        if not self.vectors:
            return []

        q_vec = np.array(query_vector, dtype=np.float32)
        scores = []

        for idx, doc_vec in enumerate(self.vectors):
            similarity = self.cosine_similarity(q_vec, doc_vec)
            scores.append((idx, similarity))

        # Sort by similarity score in descending order
        scores.sort(key=lambda x: x[1], reverse=True)
        top_scores = scores[:top_k]

        results = []
        for idx, score in top_scores:
            results.append({
                "content": self.chunks[idx],
                "score": score,
                "metadata": self.metadata[idx]
            })
            
        return results

    def save(self, file_path: str):
        """Saves vector database index into a JSON file."""
        data = {
            "chunks": self.chunks,
            "vectors": [v.tolist() for v in self.vectors],
            "metadata": self.metadata
        }
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self, file_path: str):
        """Loads vector database index from a JSON file."""
        if not os.path.exists(file_path):
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.chunks = data.get("chunks", [])
            self.vectors = [np.array(v, dtype=np.float32) for v in data.get("vectors", [])]
            self.metadata = data.get("metadata", [])
        except Exception as e:
            print(f"Error loading vector index: {e}")
