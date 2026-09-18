# Developer B — Document Pipeline & Web Frontend

You own everything from "a PDF lands on the server" to "it's searchable in the vector store," plus the web app the student actually sees. Developer A owns the agent that answers questions — you just need to feed it clean, chunked, embedded data.

## Your Slice of the Architecture

```
                         ┌──────────────┐
                         │    FASTAPI   │
                         │   BACKEND    │  ← shared scaffold, coordinate with Dev A
                         └───────┬──────┘
                                 │
                          Document Handler
                                 │
                           ┌─────┴─────┐
                           ▼           ▼
                      PDF Extraction  Course Detection
                           │           │
                           └─────┬─────┘
                                 ▼
                           RAG Pipeline (ingestion side)
                                 │
                          ┌──────┴──────┐
                          ▼             ▼
                     Vector Store   Metadata DB   ← you write to these,
                     (write)        (write)          Dev A reads from them
```

Plus the whole web app on top:

```
┌────────────────────────────────────────────────┐
│             🎓 Academic Agent                  │
│                                                │
│  Your academic materials, understood.         │
├────────────────────────────────────────────────┤
│                                                │
│  📚 Upload Academic Material                   │
│                                                │
│  [ Drag PDF here ]                             │
│                                                │
│  Course: [ CSC301 ▼ ]                          │
│                                                │
│  ────────────────────────────────────────────  │
│                                                │
│  💬 Ask your documents                         │
│                                                │
│  ┌──────────────────────────────────────────┐  │
│  │ What should I study for my test?        │  │
│  └──────────────────────────────────────────┘  │
│                                                │
│  [Ask Agent]                                   │
│                                                │
└────────────────────────────────────────────────┘
```

Keep it extremely small — one screen, upload + ask.

## Flow You're Responsible For — Flow 1 (Upload)

```
Student
   ↓
Upload PDF
   ↓
POST /documents
   ↓
FastAPI
   ↓
Document Handler
   ↓
Extract text
   ↓
Detect course
   ↓
Chunk
   ↓
Embed
   ↓
Vector Store
   ↓
Metadata DB
```

Frontend then shows:

```
✅ CSC301_Week4.pdf processed successfully.

Topics found:
CPU Scheduling
Process Management
Deadlocks
```

You're also responsible for wiring the "Ask" box in the UI to Developer A's `POST /chat` endpoint and rendering the returned answer + source.

## Endpoints You Build

```
POST   /documents/upload
GET    /documents
GET    /courses
```

(`POST /chat` and `GET /health` belong to Developer A — you just call `/chat` from the frontend.)

## Files You Own

```
backend/
├── main.py                  ← shared scaffold, coordinate with Dev A before editing
│
├── routes/
│   ├── documents.py
│   └── courses.py
│
├── rag/
│   ├── ingestion.py          # chunk + orchestrate the ingestion pipeline
│   └── embeddings.py         # embedding calls, writes to vector store
│
├── services/
│   └── pdf.py                 # PDF text extraction, course detection
│
└── models/
    └── schemas.py             # shared — coordinate with Dev A, see below

frontend/
└── app.py                     # the whole single-screen web app
```

## Build Order (4-Hour Budget)

1. `services/pdf.py` — extract text from a sample PDF, print it (20 min)
2. `rag/embeddings.py` — embed a text chunk, write to vector store, confirm you can read it back (30 min)
3. `rag/ingestion.py` — chunk text, detect course, run the full pipeline (30 min)
4. `routes/documents.py` — wire `POST /documents/upload` end to end, return topics found (30 min)
5. `frontend/app.py` — upload screen + success message (30 min)
6. `frontend/app.py` — ask box calling Dev A's `POST /chat`, rendering answer + source (30 min)
7. `routes/courses.py` — simple `GET /courses` list (10 min)
8. Buffer / integration testing with Dev A's chat pipeline (remaining time)

## Coordination Points with Developer A

- **`models/schemas.py`**: agree on the shape of a chunk/document record *before* either of you starts writing — this is the contract between ingestion and retrieval.
- **Vector store interface**: agree on the write-side function signature (e.g. `add_chunk(text: str, course: str, source: str, page: int)`) so it matches what Dev A queries against.
- Seed the vector store with a couple of real chunks as early as possible so Dev A isn't blocked waiting on your full pipeline.

## Later: WhatsApp

When WhatsApp is added, it becomes a second frontend calling the same `/documents/upload` and `/chat` endpoints — your ingestion pipeline and API layer don't change.
