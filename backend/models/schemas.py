from pydantic import BaseModel

class DocumentChunk(BaseModel):
    chunk_id: str
    text: str
    course_code: str
    course_name: str
    user_email: str   # <--- Added for Personalization
    source_file: str  
    page: int         

class UserCreate(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
