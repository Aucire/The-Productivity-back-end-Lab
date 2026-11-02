import pytest

from app import create_app
from config import Config
from extensions import db


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    JWT_SECRET_KEY = "test-jwt-secret"
    JWT_ACCESS_TOKEN_EXPIRES = False


@pytest.fixture
def app():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def registered_user(client):
    response = client.post(
        "/api/auth/register",
        json={
            "username": "christian",
            "email": "christian@example.com",
            "password": "TestPass123"
        }
    )
    assert response.status_code == 201
    return response.get_json()["user"]


@pytest.fixture
def auth_headers(client, registered_user):
    response = client.post(
        "/api/auth/login",
        json={
            "username": "christian",
            "password": "TestPass123"
        }
    )

    token = response.get_json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def second_user_headers(client):
    client.post(
        "/api/auth/register",
        json={
            "username": "seconduser",
            "email": "second@example.com",
            "password": "SecondPass123"
        }
    )

    response = client.post(
        "/api/auth/login",
        json={
            "username": "seconduser",
            "password": "SecondPass123"
        }
    )

    token = response.get_json()["access_token"]

    return {"Authorization": f"Bearer {token}"}
