from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.services.auth import get_current_user
from backend.services.learning_db import get_quizzes, save_quiz, get_study_plans, save_study_plan
from backend.rag.retrieval import search_documents
from backend.services.llm import generate_response

router = APIRouter(prefix="/learning", tags=["learning"])

class GenerateRequest(BaseModel):
    course_code: str
    topic: str

@router.get("/quizzes")
async def list_quizzes(current_user: str = Depends(get_current_user)):
    return {"quizzes": get_quizzes(current_user)}

@router.post("/quizzes/generate")
async def generate_and_save_quiz(req: GenerateRequest, current_user: str = Depends(get_current_user)):
    # 1. Fetch context from Vector Store
    chunks = search_documents(req.topic, current_user, req.course_code, top_k=5)
    context = "\n\n".join([c.text for c in chunks])
    if not context:
        context = "No specific documents found. Use general academic knowledge."
        
    prompt = f"You are an academic tutor. Use the following context to generate a 5-question multiple choice quiz with an answer key at the bottom. Topic: {req.topic}\n\nContext:\n{context}"
    
    quiz_content = generate_response(prompt)
    save_quiz(current_user, req.course_code, req.topic, quiz_content)
    
    return {"message": "Quiz generated", "content": quiz_content}

@router.get("/study-plans")
async def list_study_plans(current_user: str = Depends(get_current_user)):
    return {"study_plans": get_study_plans(current_user)}

@router.post("/study-plans/generate")
async def generate_and_save_study_plan(req: GenerateRequest, current_user: str = Depends(get_current_user)):
    chunks = search_documents(req.topic, current_user, req.course_code, top_k=5)
    context = "\n\n".join([c.text for c in chunks])
    if not context:
        context = "No specific documents found. Use general academic knowledge."
        
    prompt = f"You are an academic tutor. Create a structured, 3-day study plan for the topic: {req.topic}. Base it strictly on the provided context if possible.\n\nContext:\n{context}"
    
    plan_content = generate_response(prompt)
    save_study_plan(current_user, req.course_code, req.topic, plan_content)
    
    return {"message": "Study plan generated", "content": plan_content}
