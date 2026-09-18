from pydantic import BaseModel
from typing import Optional, List

# --- DEV A (CHAT) SCHEMAS ---
class ChatRequest(BaseModel):
    message: str
    course: Optional[str] = None

class Source(BaseModel):
    source_file: str
    page: Optional[int] = None
    course: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[Source]

# --- COMBINED CHUNK SCHEMA ---
class DocumentChunk(BaseModel):
    chunk_id: str
    text: str
    course_code: str
    course_name: str
    user_email: str   # <--- Added for Personalization
    source_file: str  
    page: int         

# --- DEV B (AUTH) SCHEMAS ---
class UserCreate(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
