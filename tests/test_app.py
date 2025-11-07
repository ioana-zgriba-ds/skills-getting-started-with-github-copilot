import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from app import app, activities
from fastapi.testclient import TestClient

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity():
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Ensure not already signed up
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert email in activities[activity]["participants"]
    # Try signing up again (should fail)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400

def test_unregister_from_activity():
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Ensure signed up
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]
    # Try unregistering again (should fail)
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 400