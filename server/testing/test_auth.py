def test_register_user(client):
    response = client.post(
        "/api/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "Password123"
        }
    )

    assert response.status_code == 201
    assert response.get_json()["user"]["username"] == "newuser"


def test_register_duplicate_user(client, registered_user):
    response = client.post(
        "/api/auth/register",
        json={
            "username": "christian",
            "email": "another@example.com",
            "password": "Password123"
        }
    )

    assert response.status_code == 409


def test_register_short_password(client):
    response = client.post(
        "/api/auth/register",
        json={
            "username": "shortuser",
            "email": "short@example.com",
            "password": "123"
        }
    )

    assert response.status_code == 400


def test_login_user(client, registered_user):
    response = client.post(
        "/api/auth/login",
        json={
            "username": "christian",
            "password": "TestPass123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.get_json()


def test_login_invalid_password(client, registered_user):
    response = client.post(
        "/api/auth/login",
        json={
            "username": "christian",
            "password": "WrongPassword"
        }
    )

    assert response.status_code == 401


def test_get_current_user(client, auth_headers):
    response = client.get(
        "/api/auth/me",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.get_json()["user"]["username"] == "christian"


def test_current_user_requires_token(client):
    response = client.get("/api/auth/me")

    assert response.status_code == 401
