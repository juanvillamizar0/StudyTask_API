import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to StudyTask API"


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_student(monkeypatch, tmp_path):
    students_file = tmp_path / "students.csv"

    monkeypatch.setattr(main, "STUDENTS_FILE", str(students_file))

    student_data = {
        "id": 1,
        "name": "Juan Villamizar",
        "email": "juan@email.com",
        "semester": 9
    }

    response = client.post("/students", json=student_data)

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "Juan Villamizar"


def test_create_subject(monkeypatch, tmp_path):
    subjects_file = tmp_path / "subjects.csv"

    monkeypatch.setattr(main, "SUBJECTS_FILE", str(subjects_file))

    subject_data = {
        "id": 1,
        "name": "Ingenieria Web",
        "credits": 3,
        "teacher": "Sergio Galvis"
    }

    response = client.post("/subjects", json=subject_data)

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "Ingenieria Web"


def test_create_task(monkeypatch, tmp_path):
    students_file = tmp_path / "students.csv"
    subjects_file = tmp_path / "subjects.csv"
    tasks_file = tmp_path / "tasks.csv"

    monkeypatch.setattr(main, "STUDENTS_FILE", str(students_file))
    monkeypatch.setattr(main, "SUBJECTS_FILE", str(subjects_file))
    monkeypatch.setattr(main, "TASKS_FILE", str(tasks_file))

    student_data = {
        "id": 1,
        "name": "Juan Villamizar",
        "email": "juan@email.com",
        "semester": 9
    }

    subject_data = {
        "id": 1,
        "name": "Ingenieria Web",
        "credits": 3,
        "teacher": "Sergio Galvis"
    }

    task_data = {
        "id": 1,
        "title": "Proyecto FastAPI",
        "description": "Desarrollo de API con persistencia CSV",
        "status": "pending",
        "student_id": 1,
        "subject_id": 1,
        "due_date": "2026-05-09"
    }

    client.post("/students", json=student_data)
    client.post("/subjects", json=subject_data)

    response = client.post("/tasks", json=task_data)

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Proyecto FastAPI"