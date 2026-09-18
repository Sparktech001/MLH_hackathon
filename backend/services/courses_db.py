from backend.services.supabase_client import supabase

def get_courses(user_email: str):
    res = supabase.table("courses").select("course_code, course_name").eq("user_email", user_email).execute()
    return res.data

def add_course(user_email: str, course_code: str, course_name: str):
    try:
        supabase.table("courses").insert({
            "user_email": user_email,
            "course_code": course_code,
            "course_name": course_name
        }).execute()
        return True
    except Exception as e:
        print(f"Error adding course: {e}")
        return False
