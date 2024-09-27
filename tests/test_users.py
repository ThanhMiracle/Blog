from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user():
    # Arrange: Prepare mock request data
    user_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password123"
    }
    
    # Act: Send POST request to create a user
    response = client.post("/user/", json=user_data)

    # Assert: Check if user is created successfully
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]

def test_create_user_email_exists():
    # Arrange: Use the same email for the second request
    user_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password123"
    }
    
    # Act: Send the same POST request twice to simulate email already existing
    response = client.post("/user/", json=user_data)  # First request to create user
    response = client.post("/user/", json=user_data)  # Second request to check for duplicate email
    
    # Assert: Check if error is raised for duplicate email
    assert response.status_code == 400
    assert response.json() == {"detail": "An user with this email already exists."}
