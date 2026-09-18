from fastapi import APIRouter, Depends
from backend.models.schemas import ChatRequest, ChatResponse
from backend.agent import agent
from backend.services.auth import get_current_user

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, current_user: str = Depends(get_current_user)):
    # Delegate logic entirely to the agent, passing the authenticated user!
    answer, sources = agent.run(
        message=request.message,
        course=request.course,
        user_email=current_user
    )

    return ChatResponse(
        answer=answer,
        sources=sources
    )
