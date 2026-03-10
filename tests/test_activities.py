import pytest


def test_get_activities_success(client):
    response = client.get("/activities")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 9


def test_get_activities_has_required_fields(client):
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity in data.items():
        assert isinstance(activity_name, str)
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)
        assert isinstance(activity["max_participants"], int)


def test_get_activities_contains_all_activities(client):
    response = client.get("/activities")
    data = response.json()
    
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Tennis Club",
        "Art Studio",
        "Music Ensemble",
        "Debate Team",
        "Science Club"
    ]
    
    for activity_name in expected_activities:
        assert activity_name in data


def test_get_activities_empty_participants(client):
    response = client.get("/activities")
    data = response.json()
    
    assert len(data["Science Club"]["participants"]) == 0


def test_get_activities_populated_participants(client):
    response = client.get("/activities")
    data = response.json()
    
    assert len(data["Chess Club"]["participants"]) == 2
    assert "michael@mergington.edu" in data["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in data["Chess Club"]["participants"]
    
    assert len(data["Basketball Team"]["participants"]) == 1
    assert "alex@mergington.edu" in data["Basketball Team"]["participants"]


def test_get_activities_participant_emails_are_strings(client):
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity in data.items():
        for participant in activity["participants"]:
            assert isinstance(participant, str)
            assert "@" in participant


def test_get_activities_max_participants_values(client):
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity in data.items():
        assert activity["max_participants"] > 0
        assert activity["max_participants"] <= 100


def test_get_activities_content_type(client):
    response = client.get("/activities")
    assert response.headers["content-type"] == "application/json"
