import uuid
from backend.services.pdf import extract_text_from_pdf
from backend.rag.embeddings import add_chunks_to_db

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunks.append(text[start:end])
        start += (chunk_size - overlap)
        
    return chunks

def process_pdf_and_ingest(file_bytes: bytes, filename: str, course_code: str, course_name: str, user_email: str):
    print(f"📄 Processing {filename} for {course_code} (User: {user_email})...")
    
    text = extract_text_from_pdf(file_bytes)
    if not text:
        return {"status": "error", "message": "Could not extract text from PDF."}
    
    chunks = chunk_text(text)
    
    metadatas = []
    ids = []
    
    for i, chunk in enumerate(chunks):
        chunk_id = f"{filename}_{uuid.uuid4().hex[:8]}_{i}"
        ids.append(chunk_id)
        metadatas.append({
            "course_code": course_code,
            "course_name": course_name,
            "user_email": user_email,  # <--- Inject owner email into metadata
            "source_file": filename,
            "chunk_index": i
        })
        
    add_chunks_to_db(chunks=chunks, metadatas=metadatas, ids=ids)
    
    return {
        "status": "success",
        "message": f"Processed {filename} successfully.",
        "course_code": course_code,
        "chunks_added": len(chunks)
    }
