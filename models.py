from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from enum import Enum


class TaskStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"


class Student(BaseModel):
    model_config = ConfigDict(
        title="Estudiante",
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Juan Villamizar",
                "email": "juan@email.com",
                "semester": 9,
                "is_active": True
            }
        }
    )

    id: int = Field(..., description="Identificador único del estudiante")
    name: str = Field(..., description="Nombre completo del estudiante")
    email: EmailStr = Field(..., description="Correo electrónico válido del estudiante")
    semester: int = Field(..., description="Semestre académico actual del estudiante")
    is_active: bool = Field(
        default=True,
        description="Estado del registro. Permite mantener histórico mediante eliminación lógica"
    )


class Subject(BaseModel):
    model_config = ConfigDict(
        title="Asignatura",
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Ingenieria Web",
                "credits": 3,
                "teacher": "Sergio Galvis",
                "is_active": True
            }
        }
    )

    id: int = Field(..., description="Identificador único de la asignatura")
    name: str = Field(..., description="Nombre de la asignatura")
    credits: int = Field(..., description="Número de créditos académicos")
    teacher: str = Field(..., description="Nombre del profesor encargado")
    is_active: bool = Field(
        default=True,
        description="Estado del registro. Permite mantener histórico mediante eliminación lógica"
    )


class Task(BaseModel):
    model_config = ConfigDict(
        title="Tarea",
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Proyecto FastAPI",
                "description": "Desarrollo de API con persistencia CSV",
                "status": "pending",
                "student_id": 1,
                "subject_id": 1,
                "due_date": "2026-05-09",
                "is_active": True
            }
        }
    )

    id: int = Field(..., description="Identificador único de la tarea")
    title: str = Field(..., description="Título de la tarea académica")
    description: str = Field(..., description="Descripción de la tarea académica")
    status: TaskStatus = Field(
        default=TaskStatus.pending,
        description="Estado actual de la tarea: pending, completed o cancelled"
    )
    student_id: int = Field(..., description="Identificador del estudiante asociado")
    subject_id: int = Field(..., description="Identificador de la asignatura asociada")
    due_date: Optional[str] = Field(
        default=None,
        description="Fecha opcional de entrega de la tarea"
    )
    is_active: bool = Field(
        default=True,
        description="Estado del registro. Permite mantener histórico mediante eliminación lógica"
    )