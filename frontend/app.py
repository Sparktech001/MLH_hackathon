import streamlit as st
import requests

API_URL = "http://localhost:8000"
st.set_page_config(page_title="Academic Agent", page_icon="🎓")

if "token" not in st.session_state:
    st.session_state.token = None

def login_screen():
    st.title("🎓 Login to Academic Agent")
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
    col1, col2 = st.columns([8, 2])
    with col1:
        st.title("🎓 Academic Agent")
        st.markdown("Your academic materials, securely isolated.")
    with col2:
        if st.button("Logout"):
            st.session_state.token = None
            st.rerun()

    st.divider()

    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    col1, col2 = st.columns([1, 2])

    with col1:
        st.header("📚 Upload Material")
        
        # 1. Fetch existing courses for this user
        try:
            res = requests.get(f"{API_URL}/courses", headers=headers)
            user_courses = res.json().get("courses", [])
        except:
            user_courses = []
            
        # 2. Build dropdown options
        course_options = [f"{c['course_code']} - {c['course_name']}" for c in user_courses]
        course_options.append("➕ Add New Course")
        
        selected_option = st.selectbox("Select Course:", course_options)
        
        course_code = ""
        course_name = ""
        
        # 3. Handle "Add New Course" logic vs "Select Existing"
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
                        st.error("Failed to add course (might already exist).")
                else:
                    st.warning("Please fill out both fields.")
        else:
            # Parse the selected option back into code and name
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
                        res_data = res.json()
                        st.success(f"✅ {uploaded_file.name} processed successfully.")
                        st.info(f"Chunks saved securely for your account.")
                    else:
                        st.error(f"Failed to upload document. {res.text}")
            else:
                st.warning("Please select a file first.")

    with col2:
        st.header("💬 Ask your documents")
        query = st.text_input("Example: What should I study for my test?")
        
        if st.button("Ask Agent"):
            if query:
                with st.spinner("Thinking..."):
                    try:
                        res = requests.post(f"{API_URL}/chat", json={"payload": query}, headers=headers)
                        if res.status_code == 200:
                            data = res.json()
                            st.markdown(f"> **{data.get('answer')}**")
                            st.caption(f"📄 Source: {data.get('source')}")
                        else:
                            st.error("Agent endpoint failed or Unauthorized.")
                    except Exception as e:
                        st.error("Could not connect to the backend.")
            else:
                st.warning("Please enter a question.")

if st.session_state.token:
    dashboard()
else:
    login_screen()
