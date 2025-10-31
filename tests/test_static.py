"""
Tests for static file serving and frontend integration.
"""

import pytest
from fastapi import status


def test_static_file_serving(client):
    """Test that static files are served correctly."""
    # Test HTML file
    response = client.get("/static/index.html")
    assert response.status_code == status.HTTP_200_OK
    assert "text/html" in response.headers.get("content-type", "")
    
    # Check that the HTML contains expected elements
    content = response.text
    assert "<title>Mergington High School Activities</title>" in content
    assert "activities-container" in content
    assert "signup-form" in content


def test_static_css_file(client):
    """Test that CSS file is served correctly."""
    response = client.get("/static/styles.css")
    assert response.status_code == status.HTTP_200_OK
    assert "text/css" in response.headers.get("content-type", "")
    
    # Check for some expected CSS content
    content = response.text
    assert "activity-card" in content
    assert "participants-list" in content
    assert "delete-btn" in content


def test_static_js_file(client):
    """Test that JavaScript file is served correctly."""
    response = client.get("/static/app.js")
    assert response.status_code == status.HTTP_200_OK
    assert "application/javascript" in response.headers.get("content-type", "") or \
           "text/javascript" in response.headers.get("content-type", "")
    
    # Check for some expected JavaScript content
    content = response.text
    assert "fetchActivities" in content
    assert "unregisterParticipant" in content
    assert "signup-form" in content


def test_nonexistent_static_file(client):
    """Test that non-existent static files return 404."""
    response = client.get("/static/nonexistent.txt")
    assert response.status_code == status.HTTP_404_NOT_FOUND