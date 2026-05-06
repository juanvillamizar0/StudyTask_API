from fastapi import FastAPI, HTTPException
from models import Student, Subject, Task
from operation_csv import (
    create_record,
    find_records,
    find_record_by_id,
    update_record,
    kill_record
)


tags_metadata = [
    {
        "name": "Inicio",
        "description": "Rutas generales para verificar el estado de la API."
    },
    {
        "name": "Estudiantes",
        "description": "Operaciones para crear, consultar, actualizar y eliminar estudiantes."
    },
    {
        "name": "Asignaturas",
        "description": "Operaciones para crear, consultar, actualizar y eliminar asignaturas."
    },
    {
        "name": "Tareas",
        "description": "Operaciones para crear, consultar, actualizar y eliminar tareas académicas."
    }
]


app = FastAPI(
    title="StudyTask API",
    description=(
        "API desarrollada para la materia Ingeniería Web. "
        "Permite gestionar estudiantes, asignaturas y tareas académicas mediante "
        "operaciones Find, Update, Create y Kill, con persistencia en archivos CSV."
    ),
    version="1.0.0",
    openapi_tags=tags_metadata
)


STUDENTS_FILE = "students.csv"
SUBJECTS_FILE = "subjects.csv"
TASKS_FILE = "tasks.csv"

STUDENT_FIELDS = ["id", "name", "email", "semester"]
SUBJECT_FIELDS = ["id", "name", "credits", "teacher"]
TASK_FIELDS = ["id", "title", "description", "status", "student_id", "subject_id", "due_date"]


@app.get(
    "/",
    tags=["Inicio"],
    summary="Página principal",
    description="Muestra un mensaje inicial con la información general del proyecto."
)
def home():
    return {
        "message": "Bienvenido a StudyTask API",
        "project": "Ingeniería Web",
        "description": "API para gestionar estudiantes, asignaturas y tareas académicas.",
        "logic": ["Find", "Update", "Create", "Kill"],
        "models": ["Student", "Subject", "Task"]
    }


@app.get(
    "/health",
    tags=["Inicio"],
    summary="Verificar estado de la API",
    description="Permite verificar que la API se encuentra funcionando correctamente."
)
def health_check():
    return {
        "status": "ok",
        "message": "StudyTask API se encuentra funcionando correctamente"
    }


# =========================
# ENDPOINTS DE ESTUDIANTES
# =========================

@app.post(
    "/students",
    tags=["Estudiantes"],
    summary="Crear estudiante",
    description="Registra un nuevo estudiante en el archivo CSV de estudiantes."
)
def create_student(student: Student):
    existing_student = find_record_by_id(STUDENTS_FILE, student.id)

    if existing_student:
        raise HTTPException(
            status_code=400,
            detail="El estudiante ya existe"
        )

    return create_record(
        STUDENTS_FILE,
        student.model_dump(mode="json"),
        STUDENT_FIELDS
    )


@app.get(
    "/students",
    tags=["Estudiantes"],
    summary="Buscar estudiantes",
    description="Retorna todos los estudiantes almacenados en el archivo CSV."
)
def find_students():
    return find_records(STUDENTS_FILE)


@app.get(
    "/students/{student_id}",
    tags=["Estudiantes"],
    summary="Buscar estudiante por ID",
    description="Busca un estudiante específico mediante su identificador único."
)
def find_student(student_id: int):
    student = find_record_by_id(STUDENTS_FILE, student_id)

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Estudiante no encontrado"
        )

    return student


@app.put(
    "/students/{student_id}",
    tags=["Estudiantes"],
    summary="Actualizar estudiante",
    description="Actualiza la información de un estudiante existente."
)
def update_student(student_id: int, student: Student):
    if student_id != student.id:
        raise HTTPException(
            status_code=400,
            detail="El ID del estudiante no coincide"
        )

    updated_student = update_record(
        STUDENTS_FILE,
        student_id,
        student.model_dump(mode="json"),
        STUDENT_FIELDS
    )

    if not updated_student:
        raise HTTPException(
            status_code=404,
            detail="Estudiante no encontrado"
        )

    return updated_student


@app.delete(
    "/students/{student_id}",
    tags=["Estudiantes"],
    summary="Eliminar estudiante",
    description="Elimina un estudiante del archivo CSV mediante su identificador."
)
def kill_student(student_id: int):
    deleted = kill_record(STUDENTS_FILE, student_id, STUDENT_FIELDS)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Estudiante no encontrado"
        )

    return {
        "message": "Estudiante eliminado correctamente"
    }


# =========================
# ENDPOINTS DE ASIGNATURAS
# =========================

@app.post(
    "/subjects",
    tags=["Asignaturas"],
    summary="Crear asignatura",
    description="Registra una nueva asignatura en el archivo CSV de asignaturas."
)
def create_subject(subject: Subject):
    existing_subject = find_record_by_id(SUBJECTS_FILE, subject.id)

    if existing_subject:
        raise HTTPException(
            status_code=400,
            detail="La asignatura ya existe"
        )

    return create_record(
        SUBJECTS_FILE,
        subject.model_dump(mode="json"),
        SUBJECT_FIELDS
    )


@app.get(
    "/subjects",
    tags=["Asignaturas"],
    summary="Buscar asignaturas",
    description="Retorna todas las asignaturas almacenadas en el archivo CSV."
)
def find_subjects():
    return find_records(SUBJECTS_FILE)


@app.get(
    "/subjects/{subject_id}",
    tags=["Asignaturas"],
    summary="Buscar asignatura por ID",
    description="Busca una asignatura específica mediante su identificador único."
)
def find_subject(subject_id: int):
    subject = find_record_by_id(SUBJECTS_FILE, subject_id)

    if not subject:
        raise HTTPException(
            status_code=404,
            detail="Asignatura no encontrada"
        )

    return subject


@app.put(
    "/subjects/{subject_id}",
    tags=["Asignaturas"],
    summary="Actualizar asignatura",
    description="Actualiza la información de una asignatura existente."
)
def update_subject(subject_id: int, subject: Subject):
    if subject_id != subject.id:
        raise HTTPException(
            status_code=400,
            detail="El ID de la asignatura no coincide"
        )

    updated_subject = update_record(
        SUBJECTS_FILE,
        subject_id,
        subject.model_dump(mode="json"),
        SUBJECT_FIELDS
    )

    if not updated_subject:
        raise HTTPException(
            status_code=404,
            detail="Asignatura no encontrada"
        )

    return updated_subject


@app.delete(
    "/subjects/{subject_id}",
    tags=["Asignaturas"],
    summary="Eliminar asignatura",
    description="Elimina una asignatura del archivo CSV mediante su identificador."
)
def kill_subject(subject_id: int):
    deleted = kill_record(SUBJECTS_FILE, subject_id, SUBJECT_FIELDS)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Asignatura no encontrada"
        )

    return {
        "message": "Asignatura eliminada correctamente"
    }


# =========================
# ENDPOINTS DE TAREAS
# =========================

@app.post(
    "/tasks",
    tags=["Tareas"],
    summary="Crear tarea",
    description=(
        "Registra una nueva tarea académica. "
        "La tarea solo se puede crear si el estudiante y la asignatura asociados existen."
    )
)
def create_task(task: Task):
    existing_task = find_record_by_id(TASKS_FILE, task.id)

    if existing_task:
        raise HTTPException(
            status_code=400,
            detail="La tarea ya existe"
        )

    student = find_record_by_id(STUDENTS_FILE, task.student_id)
    subject = find_record_by_id(SUBJECTS_FILE, task.subject_id)

    if not student:
        raise HTTPException(
            status_code=404,
            detail="El estudiante relacionado no existe"
        )

    if not subject:
        raise HTTPException(
            status_code=404,
            detail="La asignatura relacionada no existe"
        )

    return create_record(
        TASKS_FILE,
        task.model_dump(mode="json"),
        TASK_FIELDS
    )


@app.get(
    "/tasks",
    tags=["Tareas"],
    summary="Buscar tareas",
    description="Retorna todas las tareas académicas almacenadas en el archivo CSV."
)
def find_tasks():
    return find_records(TASKS_FILE)


@app.get(
    "/tasks/{task_id}",
    tags=["Tareas"],
    summary="Buscar tarea por ID",
    description="Busca una tarea académica específica mediante su identificador único."
)
def find_task(task_id: int):
    task = find_record_by_id(TASKS_FILE, task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Tarea no encontrada"
        )

    return task


@app.put(
    "/tasks/{task_id}",
    tags=["Tareas"],
    summary="Actualizar tarea",
    description=(
        "Actualiza la información de una tarea académica existente. "
        "También valida que el estudiante y la asignatura relacionados existan."
    )
)
def update_task(task_id: int, task: Task):
    if task_id != task.id:
        raise HTTPException(
            status_code=400,
            detail="El ID de la tarea no coincide"
        )

    student = find_record_by_id(STUDENTS_FILE, task.student_id)
    subject = find_record_by_id(SUBJECTS_FILE, task.subject_id)

    if not student:
        raise HTTPException(
            status_code=404,
            detail="El estudiante relacionado no existe"
        )

    if not subject:
        raise HTTPException(
            status_code=404,
            detail="La asignatura relacionada no existe"
        )

    updated_task = update_record(
        TASKS_FILE,
        task_id,
        task.model_dump(mode="json"),
        TASK_FIELDS
    )

    if not updated_task:
        raise HTTPException(
            status_code=404,
            detail="Tarea no encontrada"
        )

    return updated_task


@app.delete(
    "/tasks/{task_id}",
    tags=["Tareas"],
    summary="Eliminar tarea",
    description="Elimina una tarea académica del archivo CSV mediante su identificador."
)
def kill_task(task_id: int):
    deleted = kill_record(TASKS_FILE, task_id, TASK_FIELDS)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Tarea no encontrada"
        )

    return {
        "message": "Tarea eliminada correctamente"
    }