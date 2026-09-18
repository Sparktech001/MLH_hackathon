# AI Academic Agent — Adjusted Architecture (4-Hour Hackathon Build)

Given the 4-hour deadline, the right adjustment is: build the exact same backend and agent architecture, but use a **web app** as the first interface. Later, **WhatsApp** becomes another interface connected to the same FastAPI backend.

The key is to make sure you don't build the web app in a way that forces you to rewrite everything when adding WhatsApp.

## Adjusted Architecture

```
                         ┌───────────────┐
                         │    STUDENT    │
                         └───────┬───────┘
                                 │
                            WEB APP
                                 │
                                 ▼
                         ┌──────────────┐
                         │    FASTAPI   │
                         │   BACKEND    │
                         └───────┬──────┘
                                 │
                  ┌──────────────┴──────────────┐
                  │                             │
                  ▼                             ▼
            Text Handler                Document Handler
                  │                             │
                  │                       ┌─────┴─────┐
                  │                       ▼           ▼
                  │                  PDF Extraction  Course Detection
                  │                       │           │
                  │                       └─────┬─────┘
                  │                             ▼
                  │                       RAG Pipeline
                  │                             │
                  │                      ┌──────┴──────┐
                  │                      ▼             ▼
                  │                 Vector Store   Metadata DB
                  │                      │             │
                  └──────────────────────┼─────────────┘
                                         ▼
                                  ┌─────────────┐
                                  │  AI AGENT   │
                                  │ Orchestrator│
                                  └──────┬──────┘
                                         │
                            ┌────────────┼────────────┐
                            ▼            ▼            ▼
                         Search        Quiz       Study Plan
                        Documents
                            │
                            ▼
                       Vector Store
                            │
                            ▼
                         LLM / RAG
                            │
                            ▼
                         Response
                            │
                            ▼
                         WEB APP
```

## The Important Part

Your frontend is only the interface.

Your actual product is:

```
                 ┌────────────────────┐
                 │   AI ACADEMIC      │
                 │      AGENT         │
                 └─────────┬──────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
           Documents    Retrieval     Tools
              │            │            │
              └────────────┼────────────┘
                           ▼
                         LLM
```

Then later:

```
                 ┌────────────────────┐
                 │   AI ACADEMIC      │
                 │      AGENT         │
                 └─────────┬──────────┘
                           │
                 ┌─────────┴──────────┐
                 ▼                    ▼
              WEB APP             WHATSAPP
```

So adding WhatsApp later won't require rebuilding the agent.

## What the Web App Should Do

Keep it extremely small.

**Screen**

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

That's enough.

## Your Two Main Flows

### Flow 1 — Upload

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

### Flow 2 — Ask

Student:

> "Explain Round Robin scheduling."

```
Web App
   ↓
POST /chat
   ↓
FastAPI
   ↓
AI Agent
   ↓
Search Documents Tool
   ↓
Vector Store
   ↓
Relevant chunks
   ↓
LLM
   ↓
Answer
   ↓
Web App
```

The answer can include:

> **Round Robin Scheduling**
>
> According to your CSC301 lecture notes, Round Robin assigns each process a fixed time quantum...
>
> 📄 Source: CSC301 Week 4, page 7.

That source reference will make the demo feel much more credible.

## API Structure

Keep your backend simple:

```
POST   /documents/upload
GET    /documents
POST   /chat
GET    /courses
GET    /health
```

Later, when WhatsApp comes:

```
POST   /webhooks/whatsapp
```

That's basically it. The WhatsApp endpoint becomes another way of calling the same internal services.

## Recommended Project Structure

```
academic-agent/
│
├── backend/
│   ├── main.py
│   │
│   ├── routes/
│   │   ├── documents.py
│   │   ├── chat.py
│   │   └── courses.py
│   │
│   ├── agent/
│   │   ├── agent.py
│   │   ├── prompts.py
│   │   └── tools.py
│   │
│   ├── rag/
│   │   ├── ingestion.py
│   │   ├── retrieval.py
│   │   └── embeddings.py
│   │
│   ├── services/
│   │   ├── pdf.py
│   │   └── llm.py
│   │
│   └── models/
│       └── schemas.py
│
├── frontend/
│   └── app.py
│
├── data/
│   ├── documents/
│   └── vector_store/
│
├── .env
├── requirements.txt
└── README.md
```

For a 4-hour hackathon, you can simplify this even further if necessary.

## Then WhatsApp Becomes Easy Conceptually

Your final architecture becomes:

```
                    ┌─────────────┐
                    │   STUDENT   │
                    └──────┬──────┘
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
             WEB APP              WHATSAPP
                │                     │
                │                     │
                └──────────┬──────────┘
                           ▼
                    ┌─────────────┐
                    │   FASTAPI   │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  AI AGENT   │
                    └──────┬──────┘
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
         Documents      Database      Agent Tools
             │                           │
             ▼                           ├── Search
        Vector Store                     ├── Quiz
                                         └── Study Plan
```

That's the architecture to commit to now.

**Build the web app first**, get the complete upload → index → ask → answer loop working, and treat WhatsApp as an additional frontend/channel rather than rebuilding the system around it later.
