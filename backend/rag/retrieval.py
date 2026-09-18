from backend.models.schemas import DocumentChunk
from typing import List, Optional
from backend.rag.embeddings import query_vector_store

def search_documents(query: str, user_email: str, course: Optional[str] = None, top_k: int = 5) -> List[DocumentChunk]:
    """
    Actual implementation of vector store retrieval using ChromaDB.
    """
    try:
        raw_results = query_vector_store(query, user_email, n_results=top_k)
        
        results = []
        if not raw_results or not raw_results.get("documents") or not raw_results["documents"][0]:
            return []
            
        docs = raw_results["documents"][0]
        metadatas = raw_results["metadatas"][0]
        ids = raw_results["ids"][0]
        
        for i in range(len(docs)):
            meta = metadatas[i]
            if course and meta.get("course_code") != course and meta.get("course_name") != course:
                continue
                
            chunk = DocumentChunk(
                chunk_id=ids[i],
                text=docs[i],
                course_code=meta.get("course_code", "Unknown"),
                course_name=meta.get("course_name", "Unknown"),
                user_email=meta.get("user_email", user_email),
                source_file=meta.get("source_file", "Unknown"),
                page=meta.get("page", 1)
            )
            results.append(chunk)
            
        return results
    except Exception as e:
        print(f"Error querying vector store: {e}")
        return []
