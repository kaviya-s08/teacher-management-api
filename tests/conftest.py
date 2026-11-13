
import os

# Tell the application that pytest is running.
# This must happen before importing main.py.
os.environ["TESTING"] = "1"

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from fastapi.testclient import TestClient

from database import Base, get_db
from main import app


# --------------------------------------------------
# 1. CREATE IN-MEMORY SQLITE DATABASE
# --------------------------------------------------

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


# --------------------------------------------------
# 2. DATABASE FIXTURE
# --------------------------------------------------

@pytest.fixture
def db_session():

    Base.metadata.create_all(bind=test_engine)

    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)


# --------------------------------------------------
# 3. FASTAPI TEST CLIENT
# --------------------------------------------------

@pytest.fixture
def client(db_session):

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client

    finally:
        app.dependency_overrides.clear()


# --------------------------------------------------
# 4. AUTHENTICATED USER FIXTURE
# --------------------------------------------------

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
