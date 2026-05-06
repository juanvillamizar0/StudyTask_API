import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Bienvenido a StudyTask API"


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
        "semester": 9,
        "is_active": True
    }

    response = client.post("/students", json=student_data)

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "Juan Villamizar"
    assert response.json()["is_active"] is True


def test_filter_student_by_semester(monkeypatch, tmp_path):
    students_file = tmp_path / "students.csv"
    monkeypatch.setattr(main, "STUDENTS_FILE", str(students_file))

    student_data = {
        "id": 1,
        "name": "Juan Villamizar",
        "email": "juan@email.com",
        "semester": 9,
        "is_active": True
    }

    client.post("/students", json=student_data)

    response = client.get("/students/filter/semester/9")

    assert response.status_code == 200
    assert response.json()[0]["semester"] == "9"


def test_search_student_by_email(monkeypatch, tmp_path):
    students_file = tmp_path / "students.csv"
    monkeypatch.setattr(main, "STUDENTS_FILE", str(students_file))

    student_data = {
        "id": 1,
        "name": "Juan Villamizar",
        "email": "juan@email.com",
        "semester": 9,
        "is_active": True
    }

    client.post("/students", json=student_data)

    response = client.get("/students/search/email/juan@email.com")

    assert response.status_code == 200
    assert response.json()[0]["email"] == "juan@email.com"


def test_logical_delete_student(monkeypatch, tmp_path):
    students_file = tmp_path / "students.csv"
    monkeypatch.setattr(main, "STUDENTS_FILE", str(students_file))

    student_data = {
        "id": 1,
        "name": "Juan Villamizar",
        "email": "juan@email.com",
        "semester": 9,
        "is_active": True
    }

    client.post("/students", json=student_data)

    response = client.delete("/students/1")

    assert response.status_code == 200
    assert response.json()["student"]["is_active"] is False


def test_create_subject(monkeypatch, tmp_path):
    subjects_file = tmp_path / "subjects.csv"
    monkeypatch.setattr(main, "SUBJECTS_FILE", str(subjects_file))

    subject_data = {
        "id": 1,
        "name": "Ingenieria Web",
        "credits": 3,
        "teacher": "Sergio Galvis",
        "is_active": True
    }

    response = client.post("/subjects", json=subject_data)

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "Ingenieria Web"
    assert response.json()["is_active"] is True


def test_filter_subject_by_credits(monkeypatch, tmp_path):
    subjects_file = tmp_path / "subjects.csv"
    monkeypatch.setattr(main, "SUBJECTS_FILE", str(subjects_file))

    subject_data = {
        "id": 1,
        "name": "Ingenieria Web",
        "credits": 3,
        "teacher": "Sergio Galvis",
        "is_active": True
    }

    client.post("/subjects", json=subject_data)

    response = client.get("/subjects/filter/credits/3")

    assert response.status_code == 200
    assert response.json()[0]["credits"] == "3"


def test_search_subject_by_name(monkeypatch, tmp_path):
    subjects_file = tmp_path / "subjects.csv"
    monkeypatch.setattr(main, "SUBJECTS_FILE", str(subjects_file))

    subject_data = {
        "id": 1,
        "name": "Ingenieria Web",
        "credits": 3,
        "teacher": "Sergio Galvis",
        "is_active": True
    }

    client.post("/subjects", json=subject_data)

    response = client.get("/subjects/search/name/Ingenieria")

    assert response.status_code == 200
    assert response.json()[0]["name"] == "Ingenieria Web"


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
        "semester": 9,
        "is_active": True
    }

    subject_data = {
        "id": 1,
        "name": "Ingenieria Web",
        "credits": 3,
        "teacher": "Sergio Galvis",
        "is_active": True
    }

    task_data = {
        "id": 1,
        "title": "Proyecto FastAPI",
        "description": "Desarrollo de API con persistencia CSV",
        "status": "pending",
        "student_id": 1,
        "subject_id": 1,
        "due_date": "2026-05-09",
        "is_active": True
    }

    client.post("/students", json=student_data)
    client.post("/subjects", json=subject_data)

    response = client.post("/tasks", json=task_data)

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Proyecto FastAPI"
    assert response.json()["is_active"] is True


def test_filter_task_by_status(monkeypatch, tmp_path):
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
        "semester": 9,
        "is_active": True
    }

    subject_data = {
        "id": 1,
        "name": "Ingenieria Web",
        "credits": 3,
        "teacher": "Sergio Galvis",
        "is_active": True
    }

    task_data = {
        "id": 1,
        "title": "Proyecto FastAPI",
        "description": "Desarrollo de API con persistencia CSV",
        "status": "pending",
        "student_id": 1,
        "subject_id": 1,
        "due_date": "2026-05-09",
        "is_active": True
    }

    client.post("/students", json=student_data)
    client.post("/subjects", json=subject_data)
    client.post("/tasks", json=task_data)

    response = client.get("/tasks/filter/status/pending")

    assert response.status_code == 200
    assert response.json()[0]["status"] == "pending"


def test_search_task_by_title(monkeypatch, tmp_path):
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
        "semester": 9,
        "is_active": True
    }

    subject_data = {
        "id": 1,
        "name": "Ingenieria Web",
        "credits": 3,
        "teacher": "Sergio Galvis",
        "is_active": True
    }

    task_data = {
        "id": 1,
        "title": "Proyecto FastAPI",
        "description": "Desarrollo de API con persistencia CSV",
        "status": "pending",
        "student_id": 1,
        "subject_id": 1,
        "due_date": "2026-05-09",
        "is_active": True
    }

    client.post("/students", json=student_data)
    client.post("/subjects", json=subject_data)
    client.post("/tasks", json=task_data)

    response = client.get("/tasks/search/title/FastAPI")

    assert response.status_code == 200
    assert response.json()[0]["title"] == "Proyecto FastAPI"