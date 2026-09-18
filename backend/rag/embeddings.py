import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from backend.services.supabase_client import supabase

embeddings_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

def add_chunks_to_db(chunks: list[str], metadatas: list[dict], ids: list[str]):
    try:
        # Generate embeddings using Google Gemini
        vectors = embeddings_model.embed_documents(chunks)
        
        # Prepare for Supabase insert
        data = []
        for i, chunk_text in enumerate(chunks):
            meta = metadatas[i]
            data.append({
                "chunk_id": ids[i],
                "text": chunk_text,
                "course_code": meta.get("course_code", "Unknown"),
                "course_name": meta.get("course_name", "Unknown"),
                "user_email": meta.get("user_email"),
                "source_file": meta.get("source_file", "Unknown"),
                "page": meta.get("page", 1),
                "embedding": vectors[i]
            })
            
        # Bulk insert into Supabase
        supabase.table("document_chunks").insert(data).execute()
        print(f"✅ Successfully added {len(chunks)} chunks to Supabase Vector Store.")
    except Exception as e:
        print(f"❌ Error adding chunks to Vector Store: {e}")
        raise e

def query_vector_store(query_text: str, user_email: str, n_results: int = 3):
    """
    Queries the vector store using the custom match_documents rpc function.
    Returns a list of dicts.
    """
    query_embedding = embeddings_model.embed_query(query_text)
    
    try:
        res = supabase.rpc("match_documents", {
            "query_embedding": query_embedding,
            "match_user_email": user_email,
            "match_count": n_results
        }).execute()
        return res.data
    except Exception as e:
        print(f"Error executing vector search: {e}")
        raise e
