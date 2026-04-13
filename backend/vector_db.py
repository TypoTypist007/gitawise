from typing import List, Dict, Any
from pinecone import Pinecone
from config import settings
import logging

logger = logging.getLogger(__name__)

class VectorDBManager:
    def __init__(self):
        try:
            self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            self.index = self.pc.Index(settings.PINECONE_INDEX_NAME)
            logger.info(f"Connected to Pinecone: {settings.PINECONE_INDEX_NAME}")
        except Exception as e:
            logger.error(f"Failed to connect to Pinecone: {e}")
            raise
    
    def search_verses(self, query_embedding: List[float], top_k: int = 3) -> List[Dict[str, Any]]:
        try:
            results = self.index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
            verses = []
            for match in results.get("matches", []):
                verses.append({
                    "id": match.get("id"),
                    "score": match.get("score"),
                    "metadata": match.get("metadata", {})
                })
            return verses
        except Exception as e:
            logger.error(f"Error searching: {e}")
            return []

_vector_db_manager = None

def get_vector_db() -> VectorDBManager:
    global _vector_db_manager
    if _vector_db_manager is None:
        _vector_db_manager = VectorDBManager()
    return _vector_db_manager
