
def test_user_registration(client):

    response = client.post(
        "/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200
    assert response.json()["username"] == "newuser"


def test_duplicate_username(client):

    user_data = {
        "username": "duplicateuser",
        "email": "duplicate1@example.com",
        "password": "password123"
    }

    first_response = client.post(
        "/register",
        json=user_data
    )

    assert first_response.status_code == 200

    second_response = client.post(
        "/register",
        json={
            **user_data,
            "email": "duplicate2@example.com"
        }
    )

    assert second_response.status_code == 400


def test_invalid_registration(client):

    response = client.post(
        "/register",
        json={
            "username": "ab",
            "email": "invalid-email",
            "password": "123"
        }
    )

    assert response.status_code == 422


def test_login_success(client):

    client.post(
        "/register",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/login",
        data={
            "username": "loginuser",
            "password": "password123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_wrong_password(client):

    client.post(
        "/register",
        json={
            "username": "wronguser",
            "email": "wrong@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/login",
        data={
            "username": "wronguser",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401


def test_current_user(client, auth_headers):

    response = client.get(
        "/users/me",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


def test_missing_token(client):

    response = client.get("/users/me")

    assert response.status_code == 401


def test_invalid_token(client):

    response = client.get(
        "/users/me",
        headers={
            "Authorization": "Bearer invalid.token.value"
        }
    )

    assert response.status_code == 401
