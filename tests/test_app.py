
import pytest
from fastapi.testclient import TestClient
from src.app import app, reset_activities

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    reset_activities()

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data



def test_signup_and_unregister():
    import urllib.parse
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    activity_enc = urllib.parse.quote(activity)

    # Ensure not already registered
    client.delete(f"/activities/{activity_enc}/unregister?email={email}")

    # Sign up
    response = client.post(f"/activities/{activity_enc}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]

    # Duplicate signup should fail
    response = client.post(f"/activities/{activity_enc}/signup?email={email}")
    assert response.status_code == 400

    # Unregister
    response = client.delete(f"/activities/{activity_enc}/unregister?email={email}")
    assert response.status_code == 200
    assert f"Unregistered {email}" in response.json()["message"]

    # Unregister again should fail
    response = client.delete(f"/activities/{activity_enc}/unregister?email={email}")
    assert response.status_code == 400


def test_unregister_unknown_activity():
    unknown_activity = "UnknownActivity"
    email = "someone@mergington.edu"
    response = client.delete(f"/activities/{unknown_activity}/unregister?email={email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
