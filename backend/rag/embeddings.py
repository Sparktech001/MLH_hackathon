import chromadb
from chromadb.utils import embedding_functions
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CHROMA_DATA_PATH = os.path.join(BASE_DIR, "data", "vector_store")

client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)
embedding_func = embedding_functions.DefaultEmbeddingFunction()

collection = client.get_or_create_collection(
    name="academic_materials",
    embedding_function=embedding_func
)

def add_chunks_to_db(chunks: list[str], metadatas: list[dict], ids: list[str]):
    try:
        collection.add(documents=chunks, metadatas=metadatas, ids=ids)
        print(f"✅ Successfully added {len(chunks)} chunks to the Vector Store.")
    except Exception as e:
        print(f"❌ Error adding chunks to Vector Store: {e}")

def query_vector_store(query_text: str, user_email: str, n_results: int = 3):
    """
    Queries the vector store, filtering strictly by the user's email.
    """
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        where={"user_email": user_email}  # <--- Core Data Isolation Logic
    )
    return results
