
# src/embeddings.py
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from typing import List, Dict

class VectorStore:
    def __init__(self, persist_directory: str):
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        
    def add_documents(self, documents: List[Dict[str, str]]):
        for idx, doc in enumerate(documents):
            embeddings = self.encoder.encode(doc['content']).tolist()
            self.collection.add(
                documents=[doc['content']],
                embeddings=[embeddings],
                metadatas=[doc['metadata']],
                ids=[f"doc_{idx}"]
            )
            
    def search(self, query: str, k: int = 3) -> List[Dict]:
        query_embedding = self.encoder.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        return results
    
    def clear(self):
        """Clear all documents from the collection"""
        self.collection.delete(where={})  # Delete all documents
