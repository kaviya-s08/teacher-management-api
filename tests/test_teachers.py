
import pytest

import main
from models import Teacher


# --------------------------------------------------
# MOCK EXTERNAL SERVICES
# --------------------------------------------------

@pytest.fixture(autouse=True)
def prevent_external_services(monkeypatch):
    # Do not connect to a real Redis server during tests.
    monkeypatch.setattr(
        main,
        "clear_teacher_cache",
        lambda: None
    )

    # Do not send real emails during tests.
    monkeypatch.setattr(
        main,
        "send_teacher_registration_email",
        lambda *args, **kwargs: None
    )


# --------------------------------------------------
# STUDENT API TESTS
# --------------------------------------------------

def test_create_student(client, auth_headers):
    response = client.post(
        "/students",
        headers=auth_headers,
        json={
            "name": "Arun",
            "age": 21,
            "email": "arun@example.com",
            "course": "Python"
        }
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Arun"


def test_get_all_students(client, auth_headers):
    response = client.get(
        "/students",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_single_student_not_found(client, auth_headers):
    response = client.get(
        "/students/999999",
        headers=auth_headers
    )

    assert response.status_code == 404


def test_create_student_invalid_data(client, auth_headers):
    response = client.post(
        "/students",
        headers=auth_headers,
        json={
            "name": "",
            "age": 150,
            "email": "invalid-email",
            "course": "Python"
        }
    )

    assert response.status_code == 422


def test_access_students_without_token(client):
    response = client.get("/students")

    assert response.status_code == 401


def test_delete_student_not_found(client, auth_headers):
    response = client.delete(
        "/students/999999",
        headers=auth_headers
    )

    assert response.status_code == 404


def test_update_student(client, auth_headers):
    create_response = client.post(
        "/students",
        headers=auth_headers,
        json={
            "name": "Arun",
            "age": 21,
            "email": "arun_update@example.com",
            "course": "Python"
        }
    )

    assert create_response.status_code == 201

    student_id = create_response.json()["id"]

    update_response = client.put(
        f"/students/{student_id}",
        headers=auth_headers,
        json={
            "name": "Arun Kumar",
            "age": 22,
            "email": "arun_update@example.com",
            "course": "Java"
        }
    )

    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Arun Kumar"
    assert update_response.json()["course"] == "Java"


def test_delete_student(client, auth_headers):
    create_response = client.post(
        "/students",
        headers=auth_headers,
        json={
            "name": "Priya",
            "age": 20,
            "email": "priya_delete@example.com",
            "course": "Python"
        }
    )

    assert create_response.status_code == 201

    student_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/students/{student_id}",
        headers=auth_headers
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Student deleted successfully"

    get_response = client.get(
        f"/students/{student_id}",
        headers=auth_headers
    )

    assert get_response.status_code == 404


def test_get_existing_student(client, auth_headers):
    create_response = client.post(
        "/students",
        headers=auth_headers,
        json={
            "name": "Divya",
            "age": 21,
            "email": "divya_get@example.com",
            "course": "Python"
        }
    )

    assert create_response.status_code == 201

    student_id = create_response.json()["id"]

    response = client.get(
        f"/students/{student_id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Divya"


# --------------------------------------------------
# TEACHER API TESTS
# --------------------------------------------------

def test_create_teacher(client, auth_headers):
    response = client.post(
        "/teachers",
        headers=auth_headers,
        json={
            "name": "Arun Kumar",
            "email": "arun.teacher@example.com"
        }
    )

    assert response.status_code == 201
    assert response.json()["teacher"]["name"] == "Arun Kumar"
    assert response.json()["teacher"]["email"] == "arun.teacher@example.com"


def test_create_teacher_invalid_email(client, auth_headers):
    response = client.post(
        "/teachers",
        headers=auth_headers,
        json={
            "name": "Arun Kumar",
            "email": "invalid-email"
        }
    )

    assert response.status_code == 422


def test_create_duplicate_teacher(client, auth_headers):
    teacher_data = {
        "name": "Priya",
        "email": "priya.teacher@example.com"
    }

    first_response = client.post(
        "/teachers",
        headers=auth_headers,
        json=teacher_data
    )

    second_response = client.post(
        "/teachers",
        headers=auth_headers,
        json=teacher_data
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_update_teacher(client, auth_headers):
    create_response = client.post(
        "/teachers",
        headers=auth_headers,
        json={
            "name": "Arun",
            "email": "arun_update_teacher@example.com"
        }
    )

    assert create_response.status_code == 201

    teacher_id = create_response.json()["teacher"]["id"]

    update_response = client.put(
        f"/teachers/{teacher_id}",
        headers=auth_headers,
        json={
            "name": "Arun Kumar",
            "email": "arun_updated@example.com"
        }
    )

    assert update_response.status_code == 200
    assert update_response.json()["teacher"]["name"] == "Arun Kumar"
    assert update_response.json()["teacher"]["email"] == "arun_updated@example.com"


def test_update_teacher_not_found(client, auth_headers):
    response = client.put(
        "/teachers/999999",
        headers=auth_headers,
        json={
            "name": "Unknown Teacher",
            "email": "unknown@example.com"
        }
    )

    assert response.status_code == 404


def test_delete_teacher(client, auth_headers):
    create_response = client.post(
        "/teachers",
        headers=auth_headers,
        json={
            "name": "Divya",
            "email": "divya_delete_teacher@example.com"
        }
    )

    assert create_response.status_code == 201

    teacher_id = create_response.json()["teacher"]["id"]

    delete_response = client.delete(
        f"/teachers/{teacher_id}",
        headers=auth_headers
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Teacher deleted successfully"


def test_delete_teacher_not_found(client, auth_headers):
    response = client.delete(
        "/teachers/999999",
        headers=auth_headers
    )

    assert response.status_code == 404


# --------------------------------------------------
# SUBJECT API TESTS
# --------------------------------------------------

def test_create_subject(client, auth_headers):
    response = client.post(
        "/subjects",
        headers=auth_headers,
        json={
            "subject_name": "Python"
        }
    )

    assert response.status_code == 201
    assert response.json()["subject_name"] == "Python"


def test_get_all_subjects(client, auth_headers):
    client.post(
        "/subjects",
        headers=auth_headers,
        json={
            "subject_name": "Java"
        }
    )

    response = client.get(
        "/subjects",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(
        subject["subject_name"] == "Java"
        for subject in response.json()
    )


def test_create_duplicate_subject(client, auth_headers):
    subject_data = {
        "subject_name": "Database"
    }

    first_response = client.post(
        "/subjects",
        headers=auth_headers,
        json=subject_data
    )

    second_response = client.post(
        "/subjects",
        headers=auth_headers,
        json=subject_data
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_assign_subjects_to_teacher(client, auth_headers):
    teacher_response = client.post(
        "/teachers",
        headers=auth_headers,
        json={
            "name": "Kumar",
            "email": "kumar_subjects@example.com"
        }
    )

    subject_response = client.post(
        "/subjects",
        headers=auth_headers,
        json={
            "subject_name": "Machine Learning"
        }
    )

    assert teacher_response.status_code == 201
    assert subject_response.status_code == 201

    teacher_id = teacher_response.json()["teacher"]["id"]
    subject_id = subject_response.json()["id"]

    assignment_response = client.post(
        f"/teachers/{teacher_id}/subjects",
        headers=auth_headers,
        json={
            "subject_ids": [subject_id]
        }
    )

    assert assignment_response.status_code == 200
    assert assignment_response.json()["message"] == "Subjects assigned successfully"
    assert any(
        subject["id"] == subject_id
        for subject in assignment_response.json()["subjects"]
    )


def test_assign_subjects_to_missing_teacher(client, auth_headers):
    response = client.post(
        "/teachers/999999/subjects",
        headers=auth_headers,
        json={
            "subject_ids": [1]
        }
    )

    assert response.status_code == 404


def test_get_teacher_subjects(client, auth_headers):
    teacher_response = client.post(
        "/teachers",
        headers=auth_headers,
        json={
            "name": "Meena",
            "email": "meena_subjects@example.com"
        }
    )

    subject_response = client.post(
        "/subjects",
        headers=auth_headers,
        json={
            "subject_name": "Artificial Intelligence"
        }
    )

    teacher_id = teacher_response.json()["teacher"]["id"]
    subject_id = subject_response.json()["id"]

    client.post(
        f"/teachers/{teacher_id}/subjects",
        headers=auth_headers,
        json={
            "subject_ids": [subject_id]
        }
    )

    response = client.get(
        f"/teachers/{teacher_id}/subjects",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["teacher_name"] == "Meena"
    assert response.json()["subjects"][0]["subject_name"] == "Artificial Intelligence"


# --------------------------------------------------
# REDIS TESTS
# --------------------------------------------------

def test_get_teachers_from_database_when_redis_fails(
    client,
    auth_headers,
    db_session,
    monkeypatch
):
    teacher = Teacher(
        name="Redis Test Teacher",
        email="redis_test@example.com"
    )

    db_session.add(teacher)
    db_session.commit()

    def raise_redis_error():
        raise ConnectionError("Redis is unavailable")

    monkeypatch.setattr(
        main,
        "get_cached_teachers",
        raise_redis_error
    )

    monkeypatch.setattr(
        main,
        "set_cached_teachers",
        raise_redis_error
    )

    response = client.get(
        "/teachers",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Redis Test Teacher"


def test_get_teachers_from_redis_cache(
    client,
    auth_headers,
    monkeypatch
):
    cached_data = [
        {
            "id": 100,
            "name": "Cached Teacher",
            "email": "cached@example.com",
            "subjects": []
        }
    ]

    monkeypatch.setattr(
        main,
        "get_cached_teachers",
        lambda: cached_data
    )

    response = client.get(
        "/teachers",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json() == cached_data


# --------------------------------------------------
# BACKGROUND EMAIL TEST
# --------------------------------------------------

def test_teacher_registration_email_is_mocked(
    client,
    auth_headers,
    monkeypatch
):
    email_calls = []

    def fake_send_email(email, name):
        email_calls.append({
            "email": email,
            "name": name
        })

    monkeypatch.setattr(
        main,
        "send_teacher_registration_email",
        fake_send_email
    )

    response = client.post(
        "/teachers",
        headers=auth_headers,
        json={
            "name": "Email Test Teacher",
            "email": "email_test@example.com"
        }
    )

    assert response.status_code == 201

    assert email_calls == [
        {
            "email": "email_test@example.com",
            "name": "Email Test Teacher"
        }
    ]
