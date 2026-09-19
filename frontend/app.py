import streamlit as st
import requests
import threading

API_URL = "https://sabi-ai-2tmb.onrender.com"

# --- Wake up Render Server ---
def wake_up_server():
    try:
        # A short timeout ensures this doesn't block forever, but it's enough to hit Render and start the spin-up
        requests.get(f"{API_URL}/health", timeout=2)
    except:
        pass

if "server_woken" not in st.session_state:
    st.session_state.server_woken = True
    threading.Thread(target=wake_up_server, daemon=True).start()
# -----------------------------

st.set_page_config(page_title="SABI AI", page_icon="🎓", layout="wide")

# --- CUSTOM CSS ---
def inject_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }
        
        /* Background */
        .stApp {
            background-color: #0b1121;
            color: #ffffff;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #111827 !important;
            border-right: 1px solid #1f2937;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(90deg, #6b46c1 0%, #3b82f6 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: opacity 0.2s;
        }
        .stButton > button:hover {
            opacity: 0.9;
            color: white;
        }
        
        /* Inputs */
        .stTextInput > div > div > input, .stSelectbox > div > div > div {
            background-color: #1f2937;
            color: white;
            border: 1px solid #374151;
            border-radius: 8px;
        }
        
        /* File Uploader */
        [data-testid="stFileUploaderDropzone"] {
            background-color: #111827;
            border: 2px dashed #3b82f6;
            border-radius: 12px;
        }
        
        /* Expander/Cards */
        .streamlit-expanderHeader {
            background-color: #1f2937;
            border-radius: 8px;
        }
        
        /* Custom Welcome Banner */
        .welcome-banner {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            border: 1px solid #312e81;
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        
        .welcome-banner h1 {
            margin: 0;
            font-size: 2.2rem;
            font-weight: 700;
            color: #ffffff;
        }
        
        .welcome-banner p {
            color: #94a3b8;
            font-size: 1.1rem;
            margin-top: 0.5rem;
        }
        
        .badges {
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
        }
        .badge {
            background-color: rgba(59, 130, 246, 0.2);
            color: #60a5fa;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            border: 1px solid rgba(59, 130, 246, 0.3);
        }
        
        /* Stat Cards for Sidebar */
        .stat-card {
            background-color: #1f2937;
            border: 1px solid #374151;
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        .stat-card-icon {
            background-color: rgba(59, 130, 246, 0.1);
            color: #3b82f6;
            padding: 0.8rem;
            border-radius: 8px;
            font-size: 1.2rem;
        }
        
        /* Containers */
        [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
            background-color: #111827;
            padding: 20px;
            border-radius: 16px;
            border: 1px solid #1f2937;
        }
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

if "token" not in st.session_state:
    st.session_state.token = None

def login_screen():
    st.title("🎓 Login to SABI AI")
    st.write("Welcome! Please log in or register to securely access your documents.")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login", use_container_width=True):
            res = requests.post(f"{API_URL}/auth/login", data={"username": email, "password": password})
            if res.status_code == 200:
                st.session_state.token = res.json()["access_token"]
                st.rerun()
            else:
                st.error("Invalid credentials")
    with col2:
        if st.button("Register", use_container_width=True):
            res = requests.post(f"{API_URL}/auth/register", json={"email": email, "password": password})
            if res.status_code == 200:
                st.success("Registered successfully! Please click Login.")
            else:
                st.error("Registration failed. Email might already exist.")

def dashboard():
    # --- SIDEBAR NAVIGATION ---
    st.sidebar.markdown(
        """
        <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 20px;'>
            <h2 style='margin: 0; color: white;'>🎓 SABI <span style='color: #60a5fa;'>AI</span></h2>
        </div>
        """, 
        unsafe_allow_html=True
    )
    page = st.sidebar.radio("Go to", ["Chat & Upload", "📝 Quizzes", "📅 Study Plans"])
    
    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    st.sidebar.markdown("<h4 style='color: #94a3b8; font-size: 0.9rem;'>📊 Quick Stats</h4>", unsafe_allow_html=True)
    
    st.sidebar.markdown("""
        <div class="stat-card">
            <div class="stat-card-icon">📄</div>
            <div>
                <div style="font-size: 0.8rem; color: #94a3b8;">Documents Uploaded</div>
                <div style="font-weight: 600;">12</div>
            </div>
        </div>
        <div class="stat-card">
            <div class="stat-card-icon">✅</div>
            <div>
                <div style="font-size: 0.8rem; color: #94a3b8;">Quizzes Created</div>
                <div style="font-weight: 600;">5</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.divider()
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.token = None
        st.rerun()

    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    # Fetch User Courses (Shared across pages)
    try:
        res = requests.get(f"{API_URL}/courses", headers=headers)
        user_courses = res.json().get("courses", [])
    except:
        user_courses = []
    course_options = [f"{c['course_code']} - {c['course_name']}" for c in user_courses]

    # ================================
    # PAGE: CHAT & UPLOAD
    # ================================
    if page == "Chat & Upload":
        
        # Welcome Banner HTML
        st.markdown(
            """
            <div class="welcome-banner">
                <div>
                    <h1>Welcome back, Joseph 👋</h1>
                    <p>Your academic materials, securely isolated.</p>
                    <p style="font-size: 0.95rem;">Upload your documents, create quizzes, build study plans, and get AI-powered help — all in one place.</p>
                    <div class="badges">
                        <span class="badge">✨ AI Powered</span>
                        <span class="badge">🔒 Secure</span>
                        <span class="badge">🎓 Student Focused</span>
                    </div>
                </div>
                <div style="font-size: 6rem; opacity: 0.8;">📚</div>
            </div>
            """, 
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([1, 1.2])
        with col1:
            st.markdown("### ☁️ Upload Material")
            st.caption("Add your study materials (PDF) and let SABI AI do the rest.")
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Combine existing courses and "Add New Course" option
            course_options_upload = list(course_options)
            course_options_upload.append("➕ Add New Course")
            
            selected_option = st.selectbox("Select Course:", course_options_upload)
            
            course_code = ""
            course_name = ""
            
            if selected_option == "➕ Add New Course":
                st.markdown("**Create a new course:**")
                new_code = st.text_input("Course Code:", placeholder="e.g., BIO201")
                new_name = st.text_input("Course Name:", placeholder="e.g., Intro to Biology")
                if st.button("Save Course"):
                    if new_code and new_name:
                        res = requests.post(f"{API_URL}/courses", json={"course_code": new_code, "course_name": new_name}, headers=headers)
                        if res.status_code == 200:
                            st.success("Course added!")
                            st.rerun()
                        else:
                            st.error("Failed to add course.")
                    else:
                        st.warning("Please fill out both fields.")
            else:
                parts = selected_option.split(" - ", 1)
                if len(parts) == 2:
                    course_code, course_name = parts[0], parts[1]
                    
            uploaded_file = st.file_uploader("Drag PDF here", type=["pdf"])
            
            if st.button("Upload to Vector Store", use_container_width=True):
                if selected_option == "➕ Add New Course":
                    st.warning("Please save the new course first or select an existing one.")
                elif not course_code or not course_name:
                    st.warning("Please select a valid course.")
                elif uploaded_file is not None:
                    with st.spinner("Processing securely..."):
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                        data = {"course_code": course_code, "course_name": course_name}
                        
                        res = requests.post(f"{API_URL}/documents/upload", files=files, data=data, headers=headers)
                        
                        if res.status_code == 200:
                            st.success(f"✅ {uploaded_file.name} processed successfully.")
                        else:
                            st.error(f"Failed to upload document. {res.text}")
                else:
                    st.warning("Please select a file first.")

        with col2:
            st.markdown("### 💬 Ask your documents")
            st.caption("Get instant answers from your study materials.")
            st.markdown("<br>", unsafe_allow_html=True)
            
            query = st.text_input("Example: What should I study for my test?")
            
            if st.button("🚀 Ask Agent"):
                if query:
                    with st.spinner("Thinking..."):
                        try:
                            # Use course_code if a real course is selected
                            c_code = course_code if selected_option != "➕ Add New Course" else None
                            payload = {"message": query, "course": c_code}
                            
                            res = requests.post(f"{API_URL}/chat", json=payload, headers=headers)
                            if res.status_code == 200:
                                data = res.json()
                                st.info(f"**{data.get('answer')}**")
                                
                                # Show Sources
                                sources = data.get("sources", [])
                                if sources:
                                    st.caption("📄 Sources used:")
                                    for s in sources:
                                        st.caption(f"- {s.get('source_file')} (Page {s.get('page')})")
                            else:
                                st.error(f"Agent endpoint failed: {res.text}")
                        except Exception as e:
                            st.error(f"Could not connect to the backend: {e}")
                else:
                    st.warning("Please enter a question.")
            
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("### ✨ How it works")
            st.markdown("""
            **1. Upload your study materials** (PDF)<br>
            <span style="color: #94a3b8; font-size: 0.9rem;">We process and store them securely using advanced vector search.</span><br><br>
            **2. Ask questions and get AI-powered answers**<br>
            <span style="color: #94a3b8; font-size: 0.9rem;">From your own documents.</span>
            """, unsafe_allow_html=True)

    # ================================
    # PAGE: QUIZZES
    # ================================
    elif page == "📝 Quizzes":
        st.title("📝 AI Generated Quizzes")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Create a New Quiz")
            if course_options:
                selected_course = st.selectbox("Select Course", course_options, key="q_course")
                topic = st.text_input("Topic for Quiz", placeholder="e.g., Mitosis")
                if st.button("Generate Quiz", use_container_width=True):
                    if topic:
                        c_code = selected_course.split(" - ")[0]
                        with st.spinner("Generating quiz from your documents..."):
                            res = requests.post(f"{API_URL}/learning/quizzes/generate", json={"course_code": c_code, "topic": topic}, headers=headers)
                            if res.status_code == 200:
                                st.success("Quiz Generated and Saved!")
                                st.rerun()
                            else:
                                st.error(f"Failed to generate quiz. Detail: {res.text}")
                    else:
                        st.warning("Please enter a topic.")
            else:
                st.info("You need to add a course in the Upload tab first.")
                
        with col2:
            st.subheader("Your Past Quizzes")
            try:
                res = requests.get(f"{API_URL}/learning/quizzes", headers=headers)
                quizzes = res.json().get("quizzes", [])
                if not quizzes:
                    st.write("No quizzes generated yet.")
                for q in quizzes:
                    with st.expander(f"Quiz: {q['course_code']} - {q['topic']}"):
                        st.markdown(q['content'])
            except:
                st.error("Could not fetch quizzes.")

    # ================================
    # PAGE: STUDY PLANS
    # ================================
    elif page == "📅 Study Plans":
        st.title("📅 AI Study Plans")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Create a New Study Plan")
            if course_options:
                selected_course = st.selectbox("Select Course", course_options, key="sp_course")
                topic = st.text_input("Topic for Study Plan", placeholder="e.g., Final Exam Prep")
                if st.button("Generate Plan", use_container_width=True):
                    if topic:
                        c_code = selected_course.split(" - ")[0]
                        with st.spinner("Generating study plan from your documents..."):
                            res = requests.post(f"{API_URL}/learning/study-plans/generate", json={"course_code": c_code, "topic": topic}, headers=headers)
                            if res.status_code == 200:
                                st.success("Study Plan Generated and Saved!")
                                st.rerun()
                            else:
                                st.error(f"Failed to generate plan. Detail: {res.text}")
                    else:
                        st.warning("Please enter a topic.")
            else:
                st.info("You need to add a course in the Upload tab first.")
                
        with col2:
            st.subheader("Your Past Study Plans")
            try:
                res = requests.get(f"{API_URL}/learning/study-plans", headers=headers)
                plans = res.json().get("study_plans", [])
                if not plans:
                    st.write("No study plans generated yet.")
                for p in plans:
                    with st.expander(f"Plan: {p['course_code']} - {p['topic']}"):
                        st.markdown(p['content'])
            except:
                st.error("Could not fetch study plans.")

if st.session_state.token:
    dashboard()
else:
    login_screen()
