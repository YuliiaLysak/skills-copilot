import pytest


def test_unregister_success(client):
    email = "michael@mergington.edu"  # In Chess Club
    activity = "Chess Club"
    
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]


def test_unregister_removes_participant(client):
    email = "michael@mergington.edu"  # In Chess Club
    activity = "Chess Club"
    
    response = client.get("/activities")
    assert email in response.json()[activity]["participants"]
    
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    
    response = client.get("/activities")
    assert email not in response.json()[activity]["participants"]


def test_unregister_activity_not_found(client):
    email = "student@mergington.edu"
    activity = "Nonexistent Club"
    
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_unregister_student_not_signed_up(client):
    email = "notinclub@mergington.edu"
    activity = "Chess Club"
    
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"].lower()


def test_unregister_from_empty_activity(client):
    email = "student@mergington.edu"
    activity = "Science Club"  # Initially empty
    
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data


def test_unregister_and_resign_up(client):
    email = "michael@mergington.edu"
    activity = "Chess Club"
    
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    
    response = client.get("/activities")
    assert email not in response.json()[activity]["participants"]
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    response = client.get("/activities")
    assert email in response.json()[activity]["participants"]


def test_unregister_one_of_many_participants(client):
    activity = "Chess Club"
    
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": "michael@mergington.edu"}
    )
    assert response.status_code == 200
    
    response = client.get("/activities")
    participants = response.json()[activity]["participants"]
    assert "michael@mergington.edu" not in participants
    assert "daniel@mergington.edu" in participants
    assert len(participants) == 1


def test_unregister_url_encoded_activity_name(client):
    email = "emma@mergington.edu"  # In Programming Class
    activity = "Programming Class"  # Contains space
    
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 200


def test_unregister_url_encoded_email(client):
    email = "student+test@mergington.edu"
    email = "student+test@mergington.edu"
    activity = "Science Club"
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    assert response.status_code == 200


def test_unregister_responds_with_json(client):
    email = "michael@mergington.edu"
    activity = "Chess Club"
    
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert isinstance(data, dict)


def test_unregister_message_format(client):
    email = "michael@mergington.edu"
    activity = "Chess Club"
    
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"]
    assert isinstance(data["message"], str)


def test_unregister_empty_email(client):
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": ""}
    )
    
    # Should fail since empty email is not in participants
    assert response.status_code == 400
