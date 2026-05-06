from fastapi import FastAPI, HTTPException
from models import Student, Subject, Task, TaskStatus
from operation_csv import (
    create_record,
    find_records,
    find_record_by_id,
    update_record
)


tags_metadata = [
    {
        "name": "Inicio",
        "description": "Rutas generales para verificar el estado de la API."
    },
    {
        "name": "Estudiantes",
        "description": "Operaciones para crear, consultar, actualizar, filtrar y eliminar lógicamente estudiantes."
    },
    {
        "name": "Asignaturas",
        "description": "Operaciones para crear, consultar, actualizar, filtrar y eliminar lógicamente asignaturas."
    },
    {
        "name": "Tareas",
        "description": "Operaciones para crear, consultar, actualizar, filtrar y eliminar lógicamente tareas académicas."
    }
]


app = FastAPI(
    title="StudyTask API",
    description=(
        "API desarrollada para la materia Ingeniería Web. "
        "Permite gestionar estudiantes, asignaturas y tareas académicas mediante "
        "operaciones Find, Update, Create y Kill, con persistencia en archivos CSV. "
        "La eliminación se maneja de forma lógica mediante el campo is_active."
    ),
    version="1.0.0",
    openapi_tags=tags_metadata
)


STUDENTS_FILE = "students.csv"
SUBJECTS_FILE = "subjects.csv"
TASKS_FILE = "tasks.csv"

STUDENT_FIELDS = ["id", "name", "email", "semester", "is_active"]
SUBJECT_FIELDS = ["id", "name", "credits", "teacher", "is_active"]
TASK_FIELDS = [
    "id",
    "title",
    "description",
    "status",
    "student_id",
    "subject_id",
    "due_date",
    "is_active"
]


def is_active_value(value):
    if value is None or value == "":
        return True

    if isinstance(value, bool):
        return value

    return str(value).lower() in ["true", "1", "yes", "si", "sí"]


def filter_records_by_field(file_path: str, field: str, value) -> list:
    records = find_records(file_path)

    return [
        record for record in records
        if str(record.get(field, "")).lower() == str(value).lower()
    ]


def filter_records_by_active_status(file_path: str, is_active: bool) -> list:
    records = find_records(file_path)

    return [
        record for record in records
        if is_active_value(record.get("is_active")) == is_active
    ]


def search_records_contains(file_path: str, field: str, value: str) -> list:
    records = find_records(file_path)

    return [
        record for record in records
        if value.lower() in str(record.get(field, "")).lower()
    ]


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
        "models": ["Student", "Subject", "Task"],
        "persistence": "CSV",
        "logical_delete": "is_active"
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
    description="Retorna todos los estudiantes almacenados, tanto activos como inactivos."
)
def find_students():
    return find_records(STUDENTS_FILE)


@app.get(
    "/students/filter/semester/{semester}",
    tags=["Estudiantes"],
    summary="Filtrar estudiantes por semestre",
    description="Retorna los estudiantes que pertenecen a un semestre específico."
)
def filter_students_by_semester(semester: int):
    students = filter_records_by_field(STUDENTS_FILE, "semester", semester)

    if not students:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron estudiantes para el semestre indicado"
        )

    return students


@app.get(
    "/students/filter/active/{is_active}",
    tags=["Estudiantes"],
    summary="Filtrar estudiantes activos o inactivos",
    description="Retorna estudiantes según su estado lógico: activo o inactivo."
)
def filter_students_by_active_status(is_active: bool):
    students = filter_records_by_active_status(STUDENTS_FILE, is_active)

    if not students:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron estudiantes con el estado indicado"
        )

    return students


@app.get(
    "/students/search/email/{email}",
    tags=["Estudiantes"],
    summary="Buscar estudiante por correo",
    description="Busca estudiantes usando el correo electrónico como atributo diferente al ID."
)
def search_student_by_email(email: str):
    students = search_records_contains(STUDENTS_FILE, "email", email)

    if not students:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron estudiantes con el correo indicado"
        )

    return students


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
    summary="Eliminar estudiante lógicamente",
    description=(
        "No borra físicamente el estudiante del CSV. "
        "Actualiza el campo is_active a false para conservar histórico."
    )
)
def kill_student(student_id: int):
    student = find_record_by_id(STUDENTS_FILE, student_id)

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Estudiante no encontrado"
        )

    student["is_active"] = False

    updated_student = update_record(
        STUDENTS_FILE,
        student_id,
        student,
        STUDENT_FIELDS
    )

    return {
        "message": "Estudiante marcado como inactivo correctamente",
        "student": updated_student
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
    description="Retorna todas las asignaturas almacenadas, tanto activas como inactivas."
)
def find_subjects():
    return find_records(SUBJECTS_FILE)


@app.get(
    "/subjects/filter/credits/{credits}",
    tags=["Asignaturas"],
    summary="Filtrar asignaturas por créditos",
    description="Retorna asignaturas según el número de créditos académicos."
)
def filter_subjects_by_credits(credits: int):
    subjects = filter_records_by_field(SUBJECTS_FILE, "credits", credits)

    if not subjects:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron asignaturas con los créditos indicados"
        )

    return subjects


@app.get(
    "/subjects/filter/active/{is_active}",
    tags=["Asignaturas"],
    summary="Filtrar asignaturas activas o inactivas",
    description="Retorna asignaturas según su estado lógico: activa o inactiva."
)
def filter_subjects_by_active_status(is_active: bool):
    subjects = filter_records_by_active_status(SUBJECTS_FILE, is_active)

    if not subjects:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron asignaturas con el estado indicado"
        )

    return subjects


@app.get(
    "/subjects/search/name/{name}",
    tags=["Asignaturas"],
    summary="Buscar asignatura por nombre",
    description="Busca asignaturas usando el nombre como atributo diferente al ID."
)
def search_subject_by_name(name: str):
    subjects = search_records_contains(SUBJECTS_FILE, "name", name)

    if not subjects:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron asignaturas con el nombre indicado"
        )

    return subjects


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
    summary="Eliminar asignatura lógicamente",
    description=(
        "No borra físicamente la asignatura del CSV. "
        "Actualiza el campo is_active a false para conservar histórico."
    )
)
def kill_subject(subject_id: int):
    subject = find_record_by_id(SUBJECTS_FILE, subject_id)

    if not subject:
        raise HTTPException(
            status_code=404,
            detail="Asignatura no encontrada"
        )

    subject["is_active"] = False

    updated_subject = update_record(
        SUBJECTS_FILE,
        subject_id,
        subject,
        SUBJECT_FIELDS
    )

    return {
        "message": "Asignatura marcada como inactiva correctamente",
        "subject": updated_subject
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
    description="Retorna todas las tareas académicas almacenadas, tanto activas como inactivas."
)
def find_tasks():
    return find_records(TASKS_FILE)


@app.get(
    "/tasks/filter/status/{status}",
    tags=["Tareas"],
    summary="Filtrar tareas por estado",
    description="Retorna tareas según su estado: pending, completed o cancelled."
)
def filter_tasks_by_status(status: TaskStatus):
    tasks = filter_records_by_field(TASKS_FILE, "status", status.value)

    if not tasks:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron tareas con el estado indicado"
        )

    return tasks


@app.get(
    "/tasks/filter/active/{is_active}",
    tags=["Tareas"],
    summary="Filtrar tareas activas o inactivas",
    description="Retorna tareas según su estado lógico: activa o inactiva."
)
def filter_tasks_by_active_status(is_active: bool):
    tasks = filter_records_by_active_status(TASKS_FILE, is_active)

    if not tasks:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron tareas con el estado indicado"
        )

    return tasks


@app.get(
    "/tasks/search/title/{title}",
    tags=["Tareas"],
    summary="Buscar tarea por título",
    description="Busca tareas usando el título como atributo diferente al ID."
)
def search_task_by_title(title: str):
    tasks = search_records_contains(TASKS_FILE, "title", title)

    if not tasks:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron tareas con el título indicado"
        )

    return tasks


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
    summary="Eliminar tarea lógicamente",
    description=(
        "No borra físicamente la tarea del CSV. "
        "Actualiza el campo is_active a false para conservar histórico."
    )
)
def kill_task(task_id: int):
    task = find_record_by_id(TASKS_FILE, task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Tarea no encontrada"
        )

    task["is_active"] = False

    updated_task = update_record(
        TASKS_FILE,
        task_id,
        task,
        TASK_FIELDS
    )

    return {
        "message": "Tarea marcada como inactiva correctamente",
        "task": updated_task
    }