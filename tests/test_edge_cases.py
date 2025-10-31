"""
Edge case and error handling tests.
"""

import pytest
from fastapi import status


def test_missing_email_parameter_signup(client, reset_activities):
    """Test signup without email parameter."""
    activity_name = "Chess Club"
    
    response = client.post(f"/activities/{activity_name}/signup")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_missing_email_parameter_unregister(client, reset_activities):
    """Test unregister without email parameter."""
    activity_name = "Chess Club"
    
    response = client.delete(f"/activities/{activity_name}/unregister")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_empty_email_signup(client, reset_activities):
    """Test signup with empty email."""
    activity_name = "Chess Club"
    
    response = client.post(f"/activities/{activity_name}/signup?email=")
    assert response.status_code == status.HTTP_200_OK  # FastAPI allows empty strings
    
    # Check that empty email was actually added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "" in activities[activity_name]["participant"]


def test_malformed_activity_name(client, reset_activities):
    """Test with malformed activity names."""
    email = "test@mergington.edu"
    
    # Test with forward slashes
    response = client.post(f"/activities/Invalid/Activity/signup?email={email}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    # Test with special characters
    response = client.post(f"/activities/Invalid@Activity/signup?email={email}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_very_long_email(client, reset_activities):
    """Test signup with very long email."""
    activity_name = "Chess Club"
    long_email = "a" * 1000 + "@mergington.edu"
    
    response = client.post(f"/activities/{activity_name}/signup?email={long_email}")
    assert response.status_code == status.HTTP_200_OK
    
    # Verify it was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert long_email in activities[activity_name]["participant"]


def test_unicode_characters_in_email(client, reset_activities):
    """Test signup with unicode characters in email."""
    activity_name = "Chess Club"
    unicode_email = "tëst@mergington.edu"
    
    response = client.post(f"/activities/{activity_name}/signup?email={unicode_email}")
    assert response.status_code == status.HTTP_200_OK
    
    # Verify it was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert unicode_email in activities[activity_name]["participant"]


def test_case_sensitivity_activity_names(client, reset_activities):
    """Test that activity names are case sensitive."""
    email = "test@mergington.edu"
    
    # Correct case should work
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == status.HTTP_200_OK
    
    # Wrong case should fail
    response = client.post(f"/activities/chess club/signup?email={email}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    response = client.post(f"/activities/CHESS CLUB/signup?email={email}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_concurrent_signups_same_email(client, reset_activities):
    """Test multiple signups for the same email to different activities."""
    email = "multi@mergington.edu"
    
    # Sign up for multiple activities
    activities_to_join = ["Chess Club", "Programming Class", "Art Workshop"]
    
    for activity in activities_to_join:
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == status.HTTP_200_OK
    
    # Verify the email is in all activities
    activities_response = client.get("/activities")
    activities = activities_response.json()
    
    for activity in activities_to_join:
        assert email in activities[activity]["participant"]


def test_max_participants_boundary(client, reset_activities):
    """Test behavior when approaching max participants limit."""
    # Use Chess Club which has max_participants: 12 and currently has 3 participants
    activity_name = "Chess Club"
    
    # Get current participant count
    activities_response = client.get("/activities")
    activities = activities_response.json()
    current_count = len(activities[activity_name]["participant"])
    max_participants = activities[activity_name]["max_participants"]
    
    # Add participants up to the limit
    spots_available = max_participants - current_count
    
    for i in range(spots_available):
        email = f"student{i}@mergington.edu"
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == status.HTTP_200_OK
    
    # Try to add one more (should still work as we don't enforce max in backend)
    response = client.post(f"/activities/{activity_name}/signup?email=overflow@mergington.edu")
    assert response.status_code == status.HTTP_200_OK
    
    # Verify final count
    activities_response = client.get("/activities")
    activities = activities_response.json()
    final_count = len(activities[activity_name]["participant"])
    assert final_count == max_participants + 1  # One over the limit