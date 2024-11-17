def test_get_user_profile(client, auth_headers, test_user):
    response = client.get("/api/v1/me", headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["name"] == test_user["name"]
    assert "password" not in data

def test_get_user_profile_no_token(client):
    response = client.get("/api/v1/me")
    assert response.status_code == 401

def test_get_user_profile_invalid_token(client):
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/api/v1/me", headers=headers)
    assert response.status_code == 401
