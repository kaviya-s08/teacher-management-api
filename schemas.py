
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional


# Existing Student schemas
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


# New User Registration schema
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


# New User Response schema
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


# JWT Token Response schema
class Token(BaseModel):
    access_token: str
    token_type: str


# JWT Token Data schema
class TokenData(BaseModel):
    username: Optional[str] = None
