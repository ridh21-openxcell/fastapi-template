"""Posts module tests."""
import pytest
import time
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_create_post():
    """Test post creation."""
    # Use unique email and username to avoid conflicts
    timestamp = int(time.time() * 1000)
    email = f"postuser{timestamp}@example.com"
    username = f"postuser{timestamp}"
    
    # First register and login
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
    
    # Create post
    response = client.post(
        "/api/v1/posts/",
        json={
            "title": "Test Post",
            "content": "This is a test post content",
            "status": "draft"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Post"


def test_list_posts():
    """Test listing posts."""
    response = client.get("/api/v1/posts/")
    assert response.status_code == 200
    assert "items" in response.json()


def test_get_post():
    """Test getting a single post."""
    # This would require creating a post first
    # Placeholder test
    pass

