
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional


# -----------------------------
# Student Schemas
# -----------------------------

class StudentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=1, le=120)
    email: EmailStr
    course: str = Field(min_length=1, max_length=100)


class StudentUpdate(StudentCreate):
    pass


class StudentResponse(StudentCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


# -----------------------------
# User Authentication Schemas
# -----------------------------

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# -----------------------------
# Teacher Schemas
# -----------------------------

class TeacherCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr


class TeacherUpdateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr


# -----------------------------
# Subject Schemas
# -----------------------------

class SubjectCreate(BaseModel):
    subject_name: str = Field(min_length=1, max_length=100)


class SubjectResponse(BaseModel):
    id: int
    subject_name: str

    model_config = ConfigDict(from_attributes=True)


class SubjectAssignment(BaseModel):
    subject_ids: list[int] = Field(default_factory=list)
