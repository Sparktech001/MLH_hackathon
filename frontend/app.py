import streamlit as st
import requests

API_URL = "http://localhost:8000"
st.set_page_config(page_title="SABI AI", page_icon="🎓", layout="wide")

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
    st.sidebar.title("🎓 Navigation")
    page = st.sidebar.radio("Go to", ["Chat & Upload", "📝 Quizzes", "📅 Study Plans"])
    
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
        st.title("🎓 SABI AI Dashboard")
        st.markdown("Your academic materials, securely isolated.")
        st.divider()

        col1, col2 = st.columns([1, 2])
        with col1:
            st.header("📚 Upload Material")
            
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
            st.header("💬 Ask your documents")
            query = st.text_input("Example: What should I study for my test?")
            
            # Note: The ChatRequest in schemas.py requires 'message' and 'course'
            if st.button("Ask Agent"):
                if query:
                    with st.spinner("Thinking..."):
                        try:
                            # Use course_code if a real course is selected
                            c_code = course_code if selected_option != "➕ Add New Course" else None
                            payload = {"message": query, "course": c_code}
                            
                            res = requests.post(f"{API_URL}/chat", json=payload, headers=headers)
                            if res.status_code == 200:
                                data = res.json()
                                st.markdown(f"> **{data.get('answer')}**")
                                
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
                                st.error("Failed to generate quiz.")
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
                                st.error("Failed to generate plan.")
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
