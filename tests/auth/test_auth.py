"""Auth module tests."""
import pytest
import time
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.main import app
from src.database import get_db
from src.auth import models

client = TestClient(app)


@pytest.fixture
def db_session():
    """Create a test database session."""
    # In a real implementation, you'd use a test database
    # This is a placeholder
    pass


def test_register_user():
    """Test user registration."""
    # Use unique email and username to avoid conflicts
    timestamp = int(time.time() * 1000)
    email = f"test{timestamp}@example.com"
    username = f"testuser{timestamp}"
    
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": username,
            "password": "testpassword123"
        }
    )
    assert response.status_code == 201
    assert "email" in response.json()
    assert response.json()["email"] == email


def test_login_user():
    """Test user login."""
    # Use unique email and username to avoid conflicts
    timestamp = int(time.time() * 1000)
    email = f"login{timestamp}@example.com"
    username = f"loginuser{timestamp}"
    
    # First register a user
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": username,
            "password": "testpassword123"
        }
    )
    assert register_response.status_code == 201
    
    # Then login
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_get_current_user():
    """Test getting current user info."""
    # Use unique email and username to avoid conflicts
    timestamp = int(time.time() * 1000)
    email = f"me{timestamp}@example.com"
    username = f"meuser{timestamp}"
    
    # Register and login first
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": username,
            "password": "testpassword123"
        }
    )
    assert register_response.status_code == 201
    
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": "testpassword123"
        }
    )
    assert login_response.status_code == 200
    
    token = login_response.json()["access_token"]
    
    # Get current user
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == email

