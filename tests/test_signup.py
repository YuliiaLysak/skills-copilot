import pytest


def test_signup_success(client):
    email = "newstudent@mergington.edu"
    activity = "Science Club"
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]


def test_signup_adds_participant(client):
    email = "newstudent@mergington.edu"
    activity = "Science Club"
    
    response = client.get("/activities")
    assert len(response.json()[activity]["participants"]) == 0
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    response = client.get("/activities")
    assert email in response.json()[activity]["participants"]


def test_signup_activity_not_found(client):
    email = "student@mergington.edu"
    activity = "Nonexistent Club"
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_signup_duplicate_student(client):
    email = "michael@mergington.edu"  # Already in Chess Club
    activity = "Chess Club"
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower()


def test_signup_different_activities_same_student(client):
    email = "newstudent@mergington.edu"
    
    response = client.post(
        f"/activities/Science Club/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    response = client.post(
        f"/activities/Art Studio/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    response = client.get("/activities")
    data = response.json()
    assert email in data["Science Club"]["participants"]
    assert email in data["Art Studio"]["participants"]


def test_signup_url_encoded_activity_name(client):
    email = "student@mergington.edu"
    activity = "Programming Class"  # Contains space
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200


def test_signup_url_encoded_email(client):
    email = "student+test@mergington.edu"
    activity = "Science Club"
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    response = client.get("/activities")
    assert email in response.json()[activity]["participants"]


def test_signup_empty_email(client):
    response = client.post(
        "/activities/Science Club/signup",
        params={"email": ""}
    )
    
    response_get = client.get("/activities")
    assert "" in response_get.json()["Science Club"]["participants"]


def test_signup_responds_with_json(client):
    response = client.post(
        "/activities/Science Club/signup",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert isinstance(data, dict)


def test_signup_message_format(client):
    email = "newstudent@mergington.edu"
    activity = "Science Club"
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"]
    assert isinstance(data["message"], str)


def test_signup_error_detail_format(client):
    response = client.post(
        "/activities/Invalid Activity/signup",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
