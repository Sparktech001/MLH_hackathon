from fastapi import FastAPI
from routes.chat import router as chat_router

app = FastAPI(title="AI Academic Agent")

app.include_router(chat_router)

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
