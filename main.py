


from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    BackgroundTasks
)

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

from email_service import send_teacher_registration_email

# Redis cache imports
from cache_service import (
    get_cached_teachers,
    set_cached_teachers,
    clear_teacher_cache
)


# --------------------------------------------------
# 1. CREATE DATABASE TABLES
# --------------------------------------------------

Base.metadata.create_all(bind=engine)


# --------------------------------------------------
# 2. CREATE FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="Teacher Management API",
    description="Teacher and Student Management API with JWT Authentication, SQLAlchemy Relationships, Background Email Notifications and Redis Caching",
    version="6.0.0"
)

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
# 9. TEACHER REGISTRATION REQUEST MODEL
# --------------------------------------------------

class TeacherCreateRequest(BaseModel):

    name: str = Field(min_length=2, max_length=100)

    email: str = Field(min_length=5, max_length=255)


# --------------------------------------------------
# 10. TEACHER UPDATE REQUEST MODEL
# --------------------------------------------------

class TeacherUpdateRequest(BaseModel):

    name: str = Field(min_length=2, max_length=100)

    email: str = Field(min_length=5, max_length=255)


# --------------------------------------------------
# 11. REGISTER TEACHER WITH BACKGROUND EMAIL
# --------------------------------------------------

@app.post(
    "/teachers",
    status_code=status.HTTP_201_CREATED
)
def create_teacher(
    teacher_data: TeacherCreateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_teacher = Teacher(
        name=teacher_data.name,
        email=teacher_data.email
    )

    db.add(new_teacher)

    try:
        db.commit()
        db.refresh(new_teacher)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="A teacher with this email already exists"
        )

    # Clear cache after successful teacher registration
    clear_teacher_cache()

    # Schedule email notification in background
    background_tasks.add_task(
        send_teacher_registration_email,
        new_teacher.email,
        new_teacher.name
    )

    return {
        "message": "Teacher registered successfully. Email notification scheduled.",
        "teacher": {
            "id": new_teacher.id,
            "name": new_teacher.name,
            "email": new_teacher.email
        }
    }


# --------------------------------------------------
# 12. UPDATE TEACHER
# --------------------------------------------------

@app.put("/teachers/{teacher_id}")
def update_teacher(
    teacher_id: int,
    teacher_data: TeacherUpdateRequest,
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

    teacher.name = teacher_data.name
    teacher.email = teacher_data.email

    try:
        db.commit()
        db.refresh(teacher)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="A teacher with this email already exists"
        )

    # Clear cache after successful update
    clear_teacher_cache()

    return {
        "message": "Teacher updated successfully",
        "teacher": {
            "id": teacher.id,
            "name": teacher.name,
            "email": teacher.email
        }
    }


# --------------------------------------------------
# 13. DELETE TEACHER
# --------------------------------------------------

@app.delete("/teachers/{teacher_id}")
def delete_teacher(
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

    db.delete(teacher)

    try:
        db.commit()

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to delete teacher because related records exist"
        )

    # Clear cache after successful deletion
    clear_teacher_cache()

    return {
        "message": "Teacher deleted successfully",
        "id": teacher_id
    }


# --------------------------------------------------
# 14. REQUEST MODEL FOR ASSIGNING SUBJECTS
# --------------------------------------------------

class SubjectAssignment(BaseModel):

    subject_ids: list[int] = Field(default_factory=list)


# --------------------------------------------------
# 15. ASSIGN SUBJECTS TO A TEACHER
# --------------------------------------------------

@app.post("/teachers/{teacher_id}/subjects")
def assign_subjects(
    teacher_id: int,
    assignment: SubjectAssignment,
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

    subject_ids = list(set(assignment.subject_ids))

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

    existing_ids = {subject.id for subject in teacher.subjects}

    for subject in subjects:
        if subject.id not in existing_ids:
            teacher.subjects.append(subject)

    db.commit()
    db.refresh(teacher)

    # Clear cache because assigned subjects changed
    clear_teacher_cache()

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
# 16. GET SUBJECTS ASSIGNED TO A TEACHER
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
# 17. GET ALL TEACHERS WITH THEIR SUBJECTS
# --------------------------------------------------

@app.get("/teachers")
def get_all_teachers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Step 1: Check Redis cache
    cached_teachers = get_cached_teachers()

    if cached_teachers is not None:
        print("Redis Cache HIT")
        return cached_teachers

    print("Redis Cache MISS")

    # Step 2: Fetch teachers from PostgreSQL
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

    # Step 3: Store teacher data in Redis
    set_cached_teachers(result)

    return result
