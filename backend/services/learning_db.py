from backend.services.supabase_client import supabase

def get_quizzes(user_email: str):
    res = supabase.table("quizzes").select("id, course_code, topic, content").eq("user_email", user_email).order("id", desc=True).execute()
    return res.data

def save_quiz(user_email: str, course_code: str, topic: str, content: str):
    supabase.table("quizzes").insert({
        "user_email": user_email,
        "course_code": course_code,
        "topic": topic,
        "content": content
    }).execute()

def get_study_plans(user_email: str):
    res = supabase.table("study_plans").select("id, course_code, topic, content").eq("user_email", user_email).order("id", desc=True).execute()
    return res.data

def save_study_plan(user_email: str, course_code: str, topic: str, content: str):
    supabase.table("study_plans").insert({
        "user_email": user_email,
        "course_code": course_code,
        "topic": topic,
        "content": content
    }).execute()
