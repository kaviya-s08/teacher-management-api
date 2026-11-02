
import pytest
import database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from fastapi.testclient import TestClient

from database import Base, get_db
from main import app


# Create a separate in-memory SQLite database
TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


# Create a fresh database for each test
@pytest.fixture
def db_session():

    Base.metadata.create_all(bind=test_engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)


# Create FastAPI TestClient
@pytest.fixture
def client(db_session):

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# Create an authenticated user for protected API tests
@pytest.fixture
def auth_headers(client):

    registration_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword123"
    }

    register_response = client.post(
        "/register",
        json=registration_data
    )

    assert register_response.status_code == 200

    login_response = client.post(
        "/login",
        data={
            "username": "testuser",
            "password": "testpassword123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }
