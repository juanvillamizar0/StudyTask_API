from fastapi import FastAPI
from models import Student, Subject, Task

app = FastAPI(
    title="StudyTask API",
    description="API for managing students, subjects, and academic tasks.",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to StudyTask API",
        "project": "Ingeniería Web",
        "models": ["Student", "Subject", "Task"],
        "logic": ["Find", "Update", "Create", "Kill"]
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "StudyTask API is running"
    }