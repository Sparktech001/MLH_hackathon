# 🎓 SABI AI (Combined Developer A & B Guide)

**SABI AI** is an **AI academic assistant for university students** that allows them to upload their lecture notes, PDFs, and other academic materials, then **chat with an AI that understands those materials**.

The agent can:

* 📚 **Analyze academic documents** — extracts and understands uploaded PDFs.
* 🔎 **Search documents** — finds relevant information from a student's materials using RAG.
* 💬 **Answer questions** — students can ask questions and receive answers grounded in their documents.
* 🧠 **Explain concepts** — simplifies difficult topics from their lecture materials.
* 📝 **Generate quizzes** — creates questions based on what the student has studied.
* 📅 **Create study plans** — helps students organize what to study based on their materials.
* 📄 **Show sources** — points students back to the document/page where an answer came from.

> **SABI AI is an AI academic agent that turns a student's lecture materials into an interactive study partner they can chat with, search, learn from, quiz themselves with, and use to plan their studies.**

This repository contains both the frontend (Streamlit) and the backend (FastAPI) for SABI AI. The web app is the first interface, while WhatsApp can later connect to the same SABI AI agent through the FastAPI backend.

---

## 🛠️ Developer A: Backend Core & AI Agent Guide

The backend provides a RAG-powered REST API for answering student questions based on ingested documents.

### Local Setup & Installation

**1. Environment Variables**
Create a `.env` file at the root of the repository. Add your Gemini API key:
```env
GOOGLE_API_KEY="your_actual_api_key_here"
```

**2. Virtual Environment & Dependencies**
Activate your virtual environment and install dependencies:
```powershell
.\.venv\Scripts\activate.ps1
python -m pip install -r requirements.txt
```

**3. Run the Backend API**
Start the FastAPI server. Use `python -m` to prevent PATH mismatches:
```bash
python -m uvicorn backend.main:app --reload
```
The server runs at `http://127.0.0.1:8000`.

### Testing the AI Agent (Without Frontend)
You can test the RAG pipeline directly using `curl`:
```bash
curl -X POST http://127.0.0.1:8000/chat ^
     -H "Content-Type: application/json" ^
     -d "{\"message\": \"What is Round Robin?\", \"course\": \"CSC301\"}"
```

---

## 💻 Developer B: Frontend & Ingestion Guide

This explains the web interface, authentication, and the document ingestion pipeline.

### What Has Been Built
1. **Authentication:** Secure login with JWT.
2. **Course Management:** Create courses (SQLite).
3. **Ingestion Pipeline:** Parse, chunk, and embed PDFs into a local **ChromaDB** Vector Store.
4. **Data Privacy:** Vector chunks are tagged by user email.
5. **Web Frontend:** A Streamlit web app.

### How to Run the App (Full Stack)

You need **two separate terminal windows**. Ensure your virtual environment (`.\.venv\Scripts\activate.ps1`) is active in both!

**Terminal 1: Start the Backend**
```bash
python -m uvicorn backend.main:app --reload
```

**Terminal 2: Start the Frontend (Streamlit)**
```bash
streamlit run frontend/app.py
```
*(This automatically opens your browser to `http://localhost:8501`)*

### What You Can Test in the UI
1. **Registration & Login:** Register a new account (`test@school.edu`) and log in.
2. **Course Management:** Add a new course (e.g., `BIO201`).
3. **PDF Ingestion:** Select a course, drag a PDF, and click **Upload to Vector Store**. It extracts text and saves it to ChromaDB.
4. **The Ask Feature:** Type a question in the "Ask your documents" box to test the end-to-end integration!

### Data Storage Locations
- **Users & Courses**: `data/users.db` (SQLite)
- **Vector Embeddings**: `data/vector_store/` (ChromaDB)
