from fastapi import APIRouter
from models.schemas import ChatRequest, ChatResponse
from agent import agent

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # Delegate logic entirely to the agent
    answer, sources = agent.run(
        message=request.message,
        course=request.course
    )

    return ChatResponse(
        answer=answer,
        sources=sources
    )
