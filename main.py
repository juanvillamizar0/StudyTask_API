from fastapi import FastAPI, HTTPException
from models import Student, Subject, Task
from operation_csv import (
    create_record,
    find_records,
    find_record_by_id,
    update_record,
    kill_record
)

app = FastAPI(
    title="StudyTask API",
    description="API for managing students, subjects, and academic tasks using FUCK logic and CSV persistence.",
    version="1.0.0"
)

STUDENTS_FILE = "students.csv"
SUBJECTS_FILE = "subjects.csv"
TASKS_FILE = "tasks.csv"

STUDENT_FIELDS = ["id", "name", "email", "semester"]
SUBJECT_FIELDS = ["id", "name", "credits", "teacher"]
TASK_FIELDS = ["id", "title", "description", "status", "student_id", "subject_id", "due_date"]


@app.get("/")
def home():
    return {
        "message": "Welcome to StudyTask API",
        "project": "Ingeniería Web",
        "logic": ["Find", "Update", "Create", "Kill"],
        "models": ["Student", "Subject", "Task"]
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "StudyTask API is running"
    }


# STUDENTS FUCK

@app.post("/students")
def create_student(student: Student):
    existing_student = find_record_by_id(STUDENTS_FILE, student.id)

    if existing_student:
        raise HTTPException(status_code=400, detail="Student already exists")

    return create_record(
        STUDENTS_FILE,
        student.model_dump(mode="json"),
        STUDENT_FIELDS
    )


@app.get("/students")
def find_students():
    return find_records(STUDENTS_FILE)


@app.get("/students/{student_id}")
def find_student(student_id: int):
    student = find_record_by_id(STUDENTS_FILE, student_id)

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    if student_id != student.id:
        raise HTTPException(status_code=400, detail="Student ID does not match")

    updated_student = update_record(
        STUDENTS_FILE,
        student_id,
        student.model_dump(mode="json"),
        STUDENT_FIELDS
    )

    if not updated_student:
        raise HTTPException(status_code=404, detail="Student not found")

    return updated_student


@app.delete("/students/{student_id}")
def kill_student(student_id: int):
    deleted = kill_record(STUDENTS_FILE, student_id, STUDENT_FIELDS)

    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")

    return {
        "message": "Student deleted successfully"
    }


# SUBJECTS FUCK

@app.post("/subjects")
def create_subject(subject: Subject):
    existing_subject = find_record_by_id(SUBJECTS_FILE, subject.id)

    if existing_subject:
        raise HTTPException(status_code=400, detail="Subject already exists")

    return create_record(
        SUBJECTS_FILE,
        subject.model_dump(mode="json"),
        SUBJECT_FIELDS
    )


@app.get("/subjects")
def find_subjects():
    return find_records(SUBJECTS_FILE)


@app.get("/subjects/{subject_id}")
def find_subject(subject_id: int):
    subject = find_record_by_id(SUBJECTS_FILE, subject_id)

    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    return subject


@app.put("/subjects/{subject_id}")
def update_subject(subject_id: int, subject: Subject):
    if subject_id != subject.id:
        raise HTTPException(status_code=400, detail="Subject ID does not match")

    updated_subject = update_record(
        SUBJECTS_FILE,
        subject_id,
        subject.model_dump(mode="json"),
        SUBJECT_FIELDS
    )

    if not updated_subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    return updated_subject


@app.delete("/subjects/{subject_id}")
def kill_subject(subject_id: int):
    deleted = kill_record(SUBJECTS_FILE, subject_id, SUBJECT_FIELDS)

    if not deleted:
        raise HTTPException(status_code=404, detail="Subject not found")

    return {
        "message": "Subject deleted successfully"
    }


# TASKS FUCK

@app.post("/tasks")
def create_task(task: Task):
    existing_task = find_record_by_id(TASKS_FILE, task.id)

    if existing_task:
        raise HTTPException(status_code=400, detail="Task already exists")

    student = find_record_by_id(STUDENTS_FILE, task.student_id)
    subject = find_record_by_id(SUBJECTS_FILE, task.subject_id)

    if not student:
        raise HTTPException(status_code=404, detail="Related student not found")

    if not subject:
        raise HTTPException(status_code=404, detail="Related subject not found")

    return create_record(
        TASKS_FILE,
        task.model_dump(mode="json"),
        TASK_FIELDS
    )


@app.get("/tasks")
def find_tasks():
    return find_records(TASKS_FILE)


@app.get("/tasks/{task_id}")
def find_task(task_id: int):
    task = find_record_by_id(TASKS_FILE, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    if task_id != task.id:
        raise HTTPException(status_code=400, detail="Task ID does not match")

    student = find_record_by_id(STUDENTS_FILE, task.student_id)
    subject = find_record_by_id(SUBJECTS_FILE, task.subject_id)

    if not student:
        raise HTTPException(status_code=404, detail="Related student not found")

    if not subject:
        raise HTTPException(status_code=404, detail="Related subject not found")

    updated_task = update_record(
        TASKS_FILE,
        task_id,
        task.model_dump(mode="json"),
        TASK_FIELDS
    )

    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated_task


@app.delete("/tasks/{task_id}")
def kill_task(task_id: int):
    deleted = kill_record(TASKS_FILE, task_id, TASK_FIELDS)

    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "message": "Task deleted successfully"
    }