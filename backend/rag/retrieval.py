from models.schemas import DocumentChunk
from typing import List, Optional

# Fake chunks seeded to work independently of Developer B's ingestion
dummy_documents = [
    {
        "text": "Round Robin assigns each process a fixed time quantum.",
        "course": "CSC301",
        "document": "CSC301 Week 4",
        "page": 7
    },
    {
        "text": "Deadlock occurs when processes wait indefinitely for resources.",
        "course": "CSC301",
        "document": "CSC301 Week 5",
        "page": 3
    },
    {
        "text": "Photosynthesis is the process by which green plants transform light energy into chemical energy.",
        "course": "BIO101",
        "document": "Biology Textbook",
        "page": 42
    }
]

def search_documents(query: str, course: Optional[str] = None, top_k: int = 5) -> List[DocumentChunk]:
    """
    Dummy implementation of vector store retrieval.
    In Phase 6, this will be replaced with actual Vector DB queries using embeddings.
    """
    results = []
    
    # Very basic dummy "search" logic
    for doc in dummy_documents:
        # Filter by course if specified
        if course and doc["course"] != course:
            continue
            
        # Very crude "relevance" check for demonstration
        # (Real implementation will use cosine similarity on embeddings)
        query_terms = query.lower().split()
        doc_text = doc["text"].lower()
        
        # If any query term (length > 3) is in the document text, consider it relevant
        if any(term in doc_text for term in query_terms if len(term) > 3) or not query_terms:
             results.append(DocumentChunk(**doc))
             
    # Fallback: if no matches but course matched, return everything for that course
    if not results and course:
        results = [DocumentChunk(**doc) for doc in dummy_documents if doc["course"] == course]
        
    return results[:top_k]

if __name__ == "__main__":
    print("Testing Dummy Retrieval...")
    res = search_documents("What is Round Robin?", course="CSC301")
    for r in res:
        print(f"Found: {r.text} (Source: {r.document}, Page: {r.page})")
