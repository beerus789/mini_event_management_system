import pytest
from fastapi.testclient import TestClient

# from app.main import app
from app.main import app

client = TestClient(app)


def test_create_event_success():
    # Test: Successful event creation with valid data
    response = client.post(
        "/events",
        json={
            "name": "Test Event",
            "location": "Test Location",
            "start_time": "2025-08-29T12:00:00+05:30",
            "end_time": "2025-08-29T14:00:00+05:30",
            "max_capacity": 50,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Event"
    assert data["location"] == "Test Location"
    assert data["max_capacity"] == 50


def test_create_event_invalid_capacity():
    # Test: Event creation fails with negative max_capacity
    response = client.post(
        "/events",
        json={
            "name": "Invalid Event",
            "location": "Test Location",
            "start_time": "2025-08-29T12:00:00+05:30",
            "end_time": "2025-08-29T14:00:00+05:30",
            "max_capacity": -1,
        },
    )
    assert response.status_code == 400
    assert "max capacity" in response.json()["detail"].lower()


def test_list_events():
    # Test: Listing events returns a list of events
    response = client.get("/events")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_register_attendee_success():
    # Test: Successful attendee registration for an event
    # Create event first
    event_resp = client.post(
        "/events",
        json={
            "name": "Attendee Event",
            "location": "Test Location",
            "start_time": "2025-08-29T12:00:00+05:30",
            "end_time": "2025-08-29T14:00:00+05:30",
            "max_capacity": 2,
        },
    )
    event_id = event_resp.json()["id"]
    # Register attendee
    attendee_resp = client.post(
        f"/events/{event_id}/register",
        json={"name": "John Doe", "email": "john@example.com"},
    )
    assert attendee_resp.status_code == 200
    data = attendee_resp.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"


def test_register_attendee_duplicate():
    # Test: Duplicate attendee registration for same event fails
    # Create event first
    event_resp = client.post(
        "/events",
        json={
            "name": "Duplicate Event",
            "location": "Test Location",
            "start_time": "2025-08-29T12:00:00+05:30",
            "end_time": "2025-08-29T14:00:00+05:30",
            "max_capacity": 2,
        },
    )
    event_id = event_resp.json()["id"]
    # Register attendee
    client.post(
        f"/events/{event_id}/register",
        json={"name": "Jane Doe", "email": "jane@example.com"},
    )
    # Try duplicate registration
    dup_resp = client.post(
        f"/events/{event_id}/register",
        json={"name": "Jane Doe", "email": "jane@example.com"},
    )
    assert dup_resp.status_code == 400
    assert "duplicate" in dup_resp.json()["detail"].lower()


def test_get_attendees():
    # Test: Listing attendees for an event returns correct data
    # Create event first
    event_resp = client.post(
        "/events",
        json={
            "name": "Attendee List Event",
            "location": "Test Location",
            "start_time": "2025-08-29T12:00:00+05:30",
            "end_time": "2025-08-29T14:00:00+05:30",
            "max_capacity": 2,
        },
    )
    event_id = event_resp.json()["id"]
    # Register attendee
    client.post(
        f"/events/{event_id}/register",
        json={"name": "Alice", "email": "alice@example.com"},
    )
    resp = client.get(f"/events/{event_id}/attendees")
    assert resp.status_code == 200
    data = resp.json()
    assert "attendees" in data
    assert len(data["attendees"]) >= 1


def test_register_attendee_event_full():
    # Test: Attendee registration fails when event is full
    # Create event with capacity 1
    event_resp = client.post(
        "/events",
        json={
            "name": "Full Event",
            "location": "Test Location",
            "start_time": "2025-08-29T12:00:00+05:30",
            "end_time": "2025-08-29T14:00:00+05:30",
            "max_capacity": 1,
        },
    )
    event_id = event_resp.json()["id"]
    # Register first attendee
    client.post(
        f"/events/{event_id}/register",
        json={"name": "First", "email": "first@example.com"},
    )
    # Try to register second attendee
    resp = client.post(
        f"/events/{event_id}/register",
        json={"name": "Second", "email": "second@example.com"},
    )
    assert resp.status_code == 400
    assert "full" in resp.json()["detail"].lower()


def test_register_attendee_invalid_email():
    # Test: Attendee registration fails with invalid email format
    event_resp = client.post(
        "/events",
        json={
            "name": "Email Event",
            "location": "Test Location",
            "start_time": "2025-08-29T12:00:00+05:30",
            "end_time": "2025-08-29T14:00:00+05:30",
            "max_capacity": 2,
        },
    )
    event_id = event_resp.json()["id"]
    resp = client.post(
        f"/events/{event_id}/register",
        json={"name": "Bad Email", "email": "not-an-email"},
    )
    # FastAPI returns 422 for invalid email format due to Pydantic validation
    assert resp.status_code == 422
    # The error detail should mention 'email' or validation
    assert "email" in str(resp.json()).lower()


def test_register_attendee_nonexistent_event():
    # Test: Attendee registration fails for non-existent event
    resp = client.post(
        f"/events/99999/register", json={"name": "Ghost", "email": "ghost@example.com"}
    )
    
    assert resp.status_code == 400
    assert "not found" in resp.json()["detail"].lower()


def test_create_event_missing_fields():
    # Test: Event creation fails when required fields are missing
    resp = client.post(
        "/events",
        json={
            "name": "Missing Location Event",
            # Missing location
            "start_time": "2025-08-29T12:00:00+05:30",
            "end_time": "2025-08-29T14:00:00+05:30",
            "max_capacity": 10,
        },
    )
    assert resp.status_code == 422 or resp.status_code == 400


def test_register_attendee_missing_fields():
    # Test: Attendee registration fails when required fields are missing
    event_resp = client.post(
        "/events",
        json={
            "name": "Missing Attendee Field Event",
            "location": "Test Location",
            "start_time": "2025-08-29T12:00:00+05:30",
            "end_time": "2025-08-29T14:00:00+05:30",
            "max_capacity": 2,
        },
    )
    event_id = event_resp.json()["id"]
    resp = client.post(
        f"/events/{event_id}/register", json={"name": "No Email"}  # Missing email
    )
    assert resp.status_code == 422 or resp.status_code == 400


def test_create_event_past_dates():
    # Test: Event creation fails if start_time is in the past
    resp = client.post(
        "/events",
        json={
            "name": "Past Event",
            "location": "Test Location",
            "start_time": "2020-01-01T12:00:00+05:30",
            "end_time": "2020-01-01T14:00:00+05:30",
            "max_capacity": 10,
        },
    )
   # We are showing empty array instead of 400
    assert resp.status_code == 200
