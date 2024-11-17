def test_register_user(client):
    user_data = {
        "name": "New User",
        "email": "new@example.com",
        "password": "newpassword123",
        "location": "New Location",
        "about": "New About"
    }
    
    response = client.post("/api/v1/register-user", json=user_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["name"] == user_data["name"]
    assert "password" not in data

def test_register_duplicate_email(client, test_user):
    user_data = {
        "name": "Another User",
        "email": test_user["email"],  
        "password": "password123",
        "location": "Location",
        "about": "About"
    }
    
    response = client.post("/api/v1/register-user", json=user_data)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_login_success(client, test_user):
    login_data = {
        "email": test_user["email"],
        "password": test_user["password"]
    }
    
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    login_data = {
        "email": "wrong@example.com",
        "password": "wrongpassword"
    }
    
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 401

def test_refresh_token(client, test_user):
    # First, get tokens through logim
    login_data = {
        "email": test_user["email"],
        "password": test_user["password"]
    }
    login_response = client.post("/api/v1/auth/login", json=login_data)
    refresh_token = login_response.json()["refresh_token"]
    
    # Then refresh_the_token
    response = client.post(
        "/api/v1/auth/refresh-token",
        json={"refresh_token": refresh_token}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()