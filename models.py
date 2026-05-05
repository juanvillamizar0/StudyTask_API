from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum


# Estado de la tarea (esto suma puntos)
class TaskStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"


# Modelo Student
class Student(BaseModel):
    id: int
    name: str
    email: EmailStr
    semester: int


# Modelo Subject
class Subject(BaseModel):
    id: int
    name: str
    credits: int
    teacher: str


# Modelo Task
class Task(BaseModel):
    id: int
    title: str
    description: str
    status: TaskStatus = TaskStatus.pending
    student_id: int
    subject_id: int
    due_date: Optional[str] = None