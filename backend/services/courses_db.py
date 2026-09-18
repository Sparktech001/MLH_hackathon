import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "users.db")

def init_courses_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Create the courses table, linked to the user's email
    c.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            course_code TEXT NOT NULL,
            course_name TEXT NOT NULL,
            UNIQUE(user_email, course_code)
        )
    ''')
    conn.commit()
    conn.close()

init_courses_table()

def get_courses(user_email: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT course_code, course_name FROM courses WHERE user_email=?", (user_email,))
    rows = c.fetchall()
    conn.close()
    return [{"course_code": r[0], "course_name": r[1]} for r in rows]

def add_course(user_email: str, course_code: str, course_name: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO courses (user_email, course_code, course_name) VALUES (?, ?, ?)", 
                  (user_email, course_code, course_name))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Course already exists for this user
        return False
    finally:
        conn.close()
