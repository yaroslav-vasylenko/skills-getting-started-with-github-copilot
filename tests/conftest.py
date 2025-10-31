"""
Test configuration and fixtures for FastAPI application tests.
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities data to original state before each test."""
    # Store original activities data
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participant": [
                "michael@mergington.edu",
                "daniel@mergington.edu",
                "sarah@mergington.edu" 
            ]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participant": [
                "emma@mergington.edu",
                "sophia@mergington.edu",
                "oliver@mergington.edu"
            ]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participant": [
                "john@mergington.edu",
                "olivia@mergington.edu",
                "lucy@mergington.edu"
            ]
        },
        "Soccer Team": {
            "description": "Join the school soccer team and compete in matches",
            "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 22,
            "participant": [
                "lucas@mergington.edu",
                "mia@mergington.edu",
                "ethan@mergington.edu"
            ]
        },
        "Basketball Club": {
            "description": "Practice basketball skills and play friendly games",
            "schedule": "Mondays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participant": [
                "liam@mergington.edu",
                "ava@mergington.edu",
                "nathan@mergington.edu"
            ]
        },
        "Art Workshop": {
            "description": "Explore painting, drawing, and sculpture techniques",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participant": [
                "ella@mergington.edu",
                "noah@mergington.edu",
                "isabella@mergington.edu"
            ]
        },
        "Drama Club": {
            "description": "Act, direct, and produce school plays and performances",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participant": [
                "jack@mergington.edu",
                "grace@mergington.edu",
                "alex@mergington.edu"
            ]
        },
        "Math Olympiad": {
            "description": "Prepare for math competitions and solve challenging problems",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participant": [
                "henry@mergington.edu",
                "chloe@mergington.edu",
                "sam@mergington.edu"
            ]
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific concepts",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participant": [
                "ben@mergington.edu",
                "zoe@mergington.edu",
                "lily@mergington.edu"
            ]
        }
    }
    
    # Clear and restore original activities
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Clean up after test (restore original state)
    activities.clear()
    activities.update(original_activities)