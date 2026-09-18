from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from backend.services.auth import get_current_user
from backend.services.courses_db import get_courses, add_course

router = APIRouter(prefix="/courses", tags=["courses"])

class CourseCreate(BaseModel):
    course_code: str
    course_name: str

@router.get("/")
async def list_user_courses(current_user: str = Depends(get_current_user)):
    """
    Returns a list of courses that the logged-in user has added.
    """
    courses = get_courses(current_user)
    return {"courses": courses}

@router.post("/")
async def create_user_course(course: CourseCreate, current_user: str = Depends(get_current_user)):
    """
    Adds a new course for the logged-in user.
    """
    success = add_course(current_user, course.course_code, course.course_name)
    if not success:
        raise HTTPException(status_code=400, detail="Course code already exists for this user.")
    return {"message": "Course added successfully"}
