
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

    # First create a student
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

    # Update the student
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

    # First create a student
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

    # Delete the student
    delete_response = client.delete(
        f"/students/{student_id}",
        headers=auth_headers
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Student deleted successfully"

    # Verify that the student no longer exists
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
