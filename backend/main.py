from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import documents, courses, auth
from backend.services.auth import get_current_user

app = FastAPI(title="AI Academic Agent Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(courses.router)

@app.post("/chat")
async def chat_endpoint(payload: dict, current_user: str = Depends(get_current_user)):
    # Developer A will implement this, but we pass them the `current_user` so they know who is asking!
    return {
        "answer": f"This is a placeholder for {current_user}! Dev A will query the Vector Store here.",
        "source": "Placeholder Source, Page 1"
    }

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Backend is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
