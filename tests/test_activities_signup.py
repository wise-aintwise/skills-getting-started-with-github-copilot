"""Tests for POST /activities/{activity_name}/signup endpoint."""

import pytest


class TestActivitySignup:
    """Test suite for signing up for activities."""
    
    def test_signup_for_activity_success(self, client):
        """Arrange-Act-Assert: Test successful signup for an activity.
        
        Arrange: Create a test client with initialized activities
        Act: Send POST request to signup with valid activity and email
        Assert: Verify response status is 200 and success message returned
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert email in response.json()["message"]
    
    def test_signup_increases_participant_count(self, client):
        """Arrange-Act-Assert: Test that signup adds participant to activity.
        
        Arrange: Create a test client and get initial participant count
        Act: Send POST request to signup, then retrieve activities
        Assert: Verify participant count increased by 1
        """
        # Arrange
        activity_name = "Programming Class"
        email = "newstudent@mergington.edu"
        
        # Get initial participant count
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        
        # Act
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Get updated participant count
        updated_response = client.get("/activities")
        updated_count = len(updated_response.json()[activity_name]["participants"])
        
        # Assert
        assert signup_response.status_code == 200
        assert updated_count == initial_count + 1
        assert email in updated_response.json()[activity_name]["participants"]
    
    def test_signup_nonexistent_activity_returns_404(self, client):
        """Arrange-Act-Assert: Test signup for non-existent activity returns 404.
        
        Arrange: Create a test client
        Act: Send POST request to signup for activity that doesn't exist
        Assert: Verify response status is 404 and error message returned
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_signup_duplicate_participant_returns_400(self, client):
        """Arrange-Act-Assert: Test duplicate signup returns 400.
        
        Arrange: Create a test client with existing participant
        Act: Try to signup with email already in activity
        Assert: Verify response status is 400 and error message returned
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "Already signed up" in response.json()["detail"]
