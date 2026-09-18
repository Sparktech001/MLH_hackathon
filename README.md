# 🎓 AI Academic Agent - Developer B Testing Guide

This guide explains everything that has been built so far and how to run and test it locally on your machine.

## 🏗️ What Has Been Built (Your Responsibilities)
1. **Authentication System:** Users can register and log in securely using JWT tokens.
2. **Course Management:** Users can create and select their own courses, saved in SQLite.
3. **Ingestion Pipeline:** Uploaded PDFs are parsed, chunked, and embedded into a local **ChromaDB** Vector Store.
4. **Data Privacy:** All Vector Store chunks are tagged with the uploading user's email, ensuring data isolation.
5. **Web Frontend:** A complete Streamlit web app with login, course creation, and PDF upload workflows.

---

## 🚀 How to Run the App

You need to open **two separate terminal windows**.

### Terminal 1: Start the Backend (FastAPI)
1. Activate the virtual environment:
   ```powershell
   .\venv\Scripts\activate
   ```
2. Start the API server:
   ```bash
   python -m uvicorn backend.main:app --reload
   ```
   *(The backend will run on `http://localhost:8000`)*

### Terminal 2: Start the Frontend (Streamlit)
1. Activate the virtual environment:
   ```powershell
   .\venv\Scripts\activate
   ```
2. Start the web app:
   ```bash
   streamlit run frontend/app.py
   ```
   *(This will automatically open your browser to `http://localhost:8501`)*

---

## 🧪 What You Can Test Right Now

Follow these steps in the Streamlit web app:

### 1. Registration & Login
- Try to access the dashboard—it will prompt you for credentials.
- Type an email (e.g., `test@school.edu`) and password.
- Click **Register**. You should see a success message.
- Click **Login**. You will be redirected to the main dashboard!

### 2. Course Management
- On the left side of the dashboard, click the Course dropdown and select **"➕ Add New Course"**.
- Enter a Course Code (e.g., `BIO201`) and Course Name (e.g., `Intro to Biology`).
- Click **Save Course**. It will save to the database and update your dropdown.

### 3. PDF Ingestion (Your Core Feature!)
- Ensure your newly created course is selected in the dropdown.
- Drag and drop a small sample PDF into the file uploader.
- Click **Upload to Vector Store**.
- Watch the spinner! The backend is extracting the text, chunking it, creating embeddings, and saving it to ChromaDB. You will see a success message telling you exactly how many chunks were generated.

### 4. The Ask Feature (Placeholder)
- Type a question into the "Ask your documents" box on the right and hit **Ask Agent**.
- *Note: Developer A is responsible for the actual AI response. You will currently see a placeholder response confirming that your authenticated request successfully hit the backend.*

---

## 📂 Where is the Data Stored?
- **Users & Courses**: Saved locally in `data/users.db` (SQLite).
- **Vector Embeddings**: Saved locally in `data/vector_store/` (ChromaDB).
