



from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import engine, Base, get_db
import models

from models import (
    Student,
    User,
    Teacher,
    Subject
)

from schemas import (
    StudentCreate,
    StudentUpdate,
    StudentResponse
)

from auth import router as auth_router, get_current_user


# --------------------------------------------------
# 1. CREATE DATABASE TABLES
# --------------------------------------------------

# Importing models above registers all models with Base.metadata.
# This creates missing tables but does not modify existing tables.

Base.metadata.create_all(bind=engine)


# --------------------------------------------------
# 2. CREATE FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="Teacher Management API",
    description="Student Management API with JWT Authentication and SQLAlchemy Relationships",
    version="3.0.0"
)


# Connect authentication APIs
app.include_router(auth_router)


# --------------------------------------------------
# 3. HOME API
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Teacher Management API is running"
    }


# --------------------------------------------------
# 4. CREATE STUDENT
# --------------------------------------------------

@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_student = Student(**student.model_dump())

    db.add(new_student)

    try:
        db.commit()
        db.refresh(new_student)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="A student with this email already exists"
        )

    return new_student


# --------------------------------------------------
# 5. VIEW ALL STUDENTS
# --------------------------------------------------

@app.get(
    "/students",
    response_model=list[StudentResponse]
)
def get_students(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return db.query(Student).order_by(Student.id).all()


# --------------------------------------------------
# 6. VIEW SINGLE STUDENT
# --------------------------------------------------

@app.get(
    "/students/{student_id}",
    response_model=StudentResponse
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# --------------------------------------------------
# 7. UPDATE STUDENT
# --------------------------------------------------

@app.put(
    "/students/{student_id}",
    response_model=StudentResponse
)
def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Update only the fields provided by the user
    update_data = student_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(student, field, value)

    try:
        db.commit()
        db.refresh(student)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="A student with this email already exists"
        )

    return student


# --------------------------------------------------
# 8. DELETE STUDENT
# --------------------------------------------------

@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Student deleted successfully",
        "id": student_id
    }


# --------------------------------------------------
# 9. REQUEST MODEL FOR ASSIGNING SUBJECTS
# --------------------------------------------------

class SubjectAssignment(BaseModel):
    subject_ids: list[int] = Field(default_factory=list)


# --------------------------------------------------
# 10. ASSIGN SUBJECTS TO A TEACHER
# --------------------------------------------------

@app.post("/teachers/{teacher_id}/subjects")
def assign_subjects(
    teacher_id: int,
    assignment: SubjectAssignment,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Find teacher
    teacher = db.query(Teacher).filter(
        Teacher.id == teacher_id
    ).first()

    if teacher is None:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    # Remove duplicate subject IDs
    subject_ids = list(set(assignment.subject_ids))

    # Find the requested subjects
    subjects = db.query(Subject).filter(
        Subject.id.in_(subject_ids)
    ).all()

    found_ids = {subject.id for subject in subjects}

    missing_ids = set(subject_ids) - found_ids

    if missing_ids:
        raise HTTPException(
            status_code=404,
            detail=f"Subjects not found: {sorted(missing_ids)}"
        )

    # Add subjects without removing existing assignments
    existing_ids = {subject.id for subject in teacher.subjects}

    for subject in subjects:
        if subject.id not in existing_ids:
            teacher.subjects.append(subject)

    db.commit()
    db.refresh(teacher)

    return {
        "message": "Subjects assigned successfully",
        "teacher_id": teacher.id,
        "teacher_name": teacher.name,
        "subjects": [
            {
                "id": subject.id,
                "subject_name": subject.subject_name
            }
            for subject in teacher.subjects
        ]
    }


# --------------------------------------------------
# 11. GET SUBJECTS ASSIGNED TO A TEACHER
# --------------------------------------------------

@app.get("/teachers/{teacher_id}/subjects")
def get_teacher_subjects(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    teacher = db.query(Teacher).filter(
        Teacher.id == teacher_id
    ).first()

    if teacher is None:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    return {
        "teacher_id": teacher.id,
        "teacher_name": teacher.name,
        "teacher_email": teacher.email,
        "subjects": [
            {
                "id": subject.id,
                "subject_name": subject.subject_name
            }
            for subject in teacher.subjects
        ]
    }


# --------------------------------------------------
# 12. GET ALL TEACHERS WITH THEIR SUBJECTS
# --------------------------------------------------

@app.get("/teachers")
def get_all_teachers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    teachers = db.query(Teacher).order_by(
        Teacher.id
    ).all()

    result = []

    for teacher in teachers:

        result.append({
            "id": teacher.id,
            "name": teacher.name,
            "email": teacher.email,
            "subjects": [
                {
                    "id": subject.id,
                    "subject_name": subject.subject_name
                }
                for subject in teacher.subjects
            ]
        })

    return result
