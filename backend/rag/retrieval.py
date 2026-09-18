from backend.models.schemas import DocumentChunk
from typing import List, Optional
from backend.rag.embeddings import query_vector_store

def search_documents(query: str, user_email: str, course: Optional[str] = None, top_k: int = 5) -> List[DocumentChunk]:
    """
    Actual implementation of vector store retrieval using Supabase pgvector.
    """
    try:
        raw_results = query_vector_store(query, user_email, n_results=top_k)
        results = []
        
        if not raw_results:
            return []
            
        for doc in raw_results:
            if course and doc.get("course_code") != course and doc.get("course_name") != course:
                continue
                
            chunk = DocumentChunk(
                chunk_id=doc.get("chunk_id", "unknown"),
                text=doc.get("text", ""),
                course_code=doc.get("course_code", "Unknown"),
                course_name=doc.get("course_name", "Unknown"),
                user_email=doc.get("user_email", user_email),
                source_file=doc.get("source_file", "Unknown"),
                page=doc.get("page", 1)
            )
            results.append(chunk)
            
        return results
    except Exception as e:
        print(f"Error querying vector store: {e}")
        raise e
