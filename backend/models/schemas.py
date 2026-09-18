from pydantic import BaseModel
from typing import Optional, List

class ChatRequest(BaseModel):
    message: str
    course: Optional[str] = None

class Source(BaseModel):
    document: str
    page: Optional[int] = None
    course: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[Source]

class DocumentChunk(BaseModel):
    text: str
    document: str
    course: str
    page: int
