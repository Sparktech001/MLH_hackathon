from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from backend.rag.ingestion import process_pdf_and_ingest
from backend.services.auth import get_current_user

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    course_code: str = Form(...),
    course_name: str = Form(...),
    current_user: str = Depends(get_current_user)  # <--- Secure this endpoint
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    file_bytes = await file.read()
    # Pass current_user to ingestion
    result = process_pdf_and_ingest(file_bytes, file.filename, course_code, course_name, current_user)
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
        
    return result

@router.get("/")
async def list_documents(current_user: str = Depends(get_current_user)):
    return {"message": f"Documents for {current_user}"}
