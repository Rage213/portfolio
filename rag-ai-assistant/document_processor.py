import re
from typing import List, Dict

class DocumentProcessor:
    """
    Handles loading text files, cleaning them, and splitting them into chunks
    suitable for generating text embeddings in a RAG pipeline.
    """

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def clean_text(self, text: str) -> str:
        """Removes duplicate whitespaces, newlines, and normalizes text structure."""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def split_into_chunks(self, text: str) -> List[str]:
        """
        Splits clean text into overlapping chunks of defined length.
        """
        cleaned = self.clean_text(text)
        if not cleaned:
            return []

        chunks = []
        start = 0
        text_len = len(cleaned)

        while start < text_len:
            end = min(start + self.chunk_size, text_len)
            
            # If we aren't at the end, try to find a natural boundary (dot, space)
            if end < text_len:
                # Look back up to 50 characters for a punctuation mark or space
                boundary = cleaned.rfind('. ', end - 50, end)
                if boundary != -1:
                    end = boundary + 1
                else:
                    boundary = cleaned.rfind(' ', end - 20, end)
                    if boundary != -1:
                        end = boundary

            chunk = cleaned[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Step forward by chunk_size - overlap
            start = end - self.chunk_overlap
            if start >= text_len or end >= text_len:
                break
                
        return chunks

    def process_file(self, file_path: str) -> List[Dict[str, any]]:
        """
        Reads a local text file and converts it into a list of structured chunks.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            chunks = self.split_into_chunks(content)
            
            return [
                {
                    "content": chunk,
                    "metadata": {
                        "source": file_path,
                        "chunk_index": i
                    }
                }
                for i, chunk in enumerate(chunks)
            ]
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            return []
