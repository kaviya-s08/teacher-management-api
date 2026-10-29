
from pydantic import BaseModel, ConfigDict, Field, EmailStr


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
