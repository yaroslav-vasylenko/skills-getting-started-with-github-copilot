"""
Tests for the main API endpoints.
"""

import pytest
from fastapi import status


def test_root_redirect(client):
    """Test that root path redirects to static HTML."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.url.path == "/static/index.html"


def test_get_activities(client, reset_activities):
    """Test getting all activities."""
    response = client.get("/activities")
    assert response.status_code == status.HTTP_200_OK
    
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) == 9  # Should have 9 activities
    
    # Check if specific activities exist
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Gym Class" in activities
    
    # Check structure of an activity
    chess_club = activities["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participant" in chess_club
    assert isinstance(chess_club["participant"], list)


def test_signup_for_activity_success(client, reset_activities):
    """Test successful signup for an activity."""
    email = "newstudent@mergington.edu"
    activity_name = "Chess Club"
    
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == status.HTTP_200_OK
    
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    assert activity_name in result["message"]
    
    # Verify the participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participant"]


def test_signup_for_nonexistent_activity(client, reset_activities):
    """Test signup for an activity that doesn't exist."""
    email = "newstudent@mergington.edu"
    activity_name = "Nonexistent Activity"
    
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    result = response.json()
    assert result["detail"] == "Activity not found"


def test_signup_duplicate_participant(client, reset_activities):
    """Test signup for an activity where student is already registered."""
    email = "michael@mergington.edu"  # Already in Chess Club
    activity_name = "Chess Club"
    
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    result = response.json()
    assert result["detail"] == "Student is already signed up"


def test_unregister_from_activity_success(client, reset_activities):
    """Test successful unregistration from an activity."""
    email = "michael@mergington.edu"  # Already in Chess Club
    activity_name = "Chess Club"
    
    # First verify the participant is in the activity
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participant"]
    
    # Unregister the participant
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == status.HTTP_200_OK
    
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    assert activity_name in result["message"]
    
    # Verify the participant was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities[activity_name]["participant"]


def test_unregister_from_nonexistent_activity(client, reset_activities):
    """Test unregistration from an activity that doesn't exist."""
    email = "michael@mergington.edu"
    activity_name = "Nonexistent Activity"
    
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    result = response.json()
    assert result["detail"] == "Activity not found"


def test_unregister_non_participant(client, reset_activities):
    """Test unregistration of a student who is not registered for the activity."""
    email = "notregistered@mergington.edu"
    activity_name = "Chess Club"
    
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    result = response.json()
    assert result["detail"] == "Student is not registered for this activity"


def test_signup_and_unregister_workflow(client, reset_activities):
    """Test complete workflow of signing up and then unregistering."""
    email = "workflow@mergington.edu"
    activity_name = "Programming Class"
    
    # Initial state - student not registered
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities[activity_name]["participant"]
    initial_count = len(activities[activity_name]["participant"])
    
    # Sign up
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == status.HTTP_200_OK
    
    # Verify signup
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participant"]
    assert len(activities[activity_name]["participant"]) == initial_count + 1
    
    # Unregister
    unregister_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert unregister_response.status_code == status.HTTP_200_OK
    
    # Verify unregistration
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities[activity_name]["participant"]
    assert len(activities[activity_name]["participant"]) == initial_count


def test_activity_data_integrity(client, reset_activities):
    """Test that activity data structure is maintained correctly."""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        # Check required fields
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participant" in activity_data
        
        # Check data types
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participant"], list)
        
        # Check constraints
        assert activity_data["max_participants"] > 0
        assert len(activity_data["participant"]) <= activity_data["max_participants"]
        
        # Check participant emails format (basic check)
        for participant in activity_data["participant"]:
            assert isinstance(participant, str)
            assert "@" in participant
            assert participant.endswith("@mergington.edu")


def test_special_characters_in_activity_names(client, reset_activities):
    """Test handling of special characters in activity names for URL encoding."""
    # Test with URL encoding
    activity_name = "Chess Club"
    encoded_name = "Chess%20Club"
    email = "test@mergington.edu"
    
    response = client.post(f"/activities/{encoded_name}/signup?email={email}")
    assert response.status_code == status.HTTP_200_OK
    
    # Verify the participant was added to the correct activity
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participant"]