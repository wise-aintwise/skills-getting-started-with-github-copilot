"""Tests for DELETE /activities/{activity_name}/unregister endpoint."""

import pytest


class TestActivityUnregister:
    """Test suite for unregistering from activities."""
    
    def test_unregister_from_activity_success(self, client):
        """Arrange-Act-Assert: Test successful unregistration from activity.
        
        Arrange: Create a test client with activities containing participants
        Act: Send DELETE request to unregister with valid activity and participant
        Assert: Verify response status is 200 and success message returned
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Existing participant
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        assert email in response.json()["message"]
    
    def test_unregister_decreases_participant_count(self, client):
        """Arrange-Act-Assert: Test that unregister removes participant from activity.
        
        Arrange: Create a test client and get initial participant count
        Act: Send DELETE request to unregister, then retrieve activities
        Assert: Verify participant count decreased by 1
        """
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"  # Existing participant
        
        # Get initial participant count
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        
        # Act
        unregister_response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Get updated participant count
        updated_response = client.get("/activities")
        updated_count = len(updated_response.json()[activity_name]["participants"])
        
        # Assert
        assert unregister_response.status_code == 200
        assert updated_count == initial_count - 1
        assert email not in updated_response.json()[activity_name]["participants"]
    
    def test_unregister_nonexistent_activity_returns_404(self, client):
        """Arrange-Act-Assert: Test unregister from non-existent activity returns 404.
        
        Arrange: Create a test client
        Act: Send DELETE request to unregister from activity that doesn't exist
        Assert: Verify response status is 404 and error message returned
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_unregister_nonexistent_participant_returns_404(self, client):
        """Arrange-Act-Assert: Test unregister for non-existent participant returns 404.
        
        Arrange: Create a test client with activities
        Act: Try to unregister email not in activity
        Assert: Verify response status is 404 and error message returned
        """
        # Arrange
        activity_name = "Chess Club"
        email = "notamember@mergington.edu"  # Not signed up for this activity
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]
