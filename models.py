

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table
)
from sqlalchemy.orm import relationship
from database import Base

teacher_subjects = Table(
    "teacher_subjects",
    Base.metadata,

    Column(
        "teacher_id",
        Integer,
        ForeignKey("teachers.id"),
        primary_key=True
    ),

    Column(
        "subject_id",
        Integer,
        ForeignKey("subjects.id"),
        primary_key=True
    )
)

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )


    students = relationship(
        "Student",
        back_populates="teacher"
    )

    profile = relationship(
        "TeacherProfile",
        back_populates="teacher",
        uselist=False,
        cascade="all, delete-orphan"
    )


    subjects = relationship(
        "Subject",
        secondary=teacher_subjects,
        back_populates="teachers"
    )

class TeacherProfile(Base):
    __tablename__ = "teacher_profiles"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    qualification = Column(
        String,
        nullable=False
    )

    experience = Column(
        Integer,
        nullable=False
    )

    teacher_id = Column(
        Integer,
        ForeignKey("teachers.id"),
        unique=True,
        nullable=False
    )

    # Connect profile to teacher

    teacher = relationship(
        "Teacher",
        back_populates="profile"
    )

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    age = Column(Integer, nullable=True)
    course = Column(String, nullable=True)

    teacher_id = Column(
        Integer,
        ForeignKey("teachers.id"),
        nullable=True
    )

    teacher = relationship(
        "Teacher",
        back_populates="students"
    )
class Subject(Base):
    __tablename__ = "subjects"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    subject_name = Column(
        String,
        unique=True,
        nullable=False
    )
    teachers = relationship(
        "Teacher",
        secondary=teacher_subjects,
        back_populates="subjects"
    )
# --------------------------------------------------
# USER MODEL - JWT AUTHENTICATION
# --------------------------------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    hashed_password = Column(
        String,
        nullable=False
    )
