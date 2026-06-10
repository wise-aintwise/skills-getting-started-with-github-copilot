"""Tests for GET /activities endpoint."""

import pytest


class TestGetActivities:
    """Test suite for retrieving all activities."""
    
    def test_get_all_activities_returns_success(self, client):
        """Arrange-Act-Assert: Test that GET /activities returns all activities.
        
        Arrange: Create a test client
        Act: Send GET request to /activities
        Assert: Verify response status is 200
        """
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
    
    def test_get_activities_returns_correct_structure(self, client):
        """Arrange-Act-Assert: Test that activities have expected structure.
        
        Arrange: Create a test client
        Act: Send GET request to /activities
        Assert: Verify each activity has required fields
        """
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert isinstance(activities, dict)
        assert len(activities) == 9
        
        # Verify structure of first activity
        chess_club = activities["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
    
    def test_get_activities_returns_correct_participants(self, client):
        """Arrange-Act-Assert: Test that activities return correct participant lists.
        
        Arrange: Create a test client
        Act: Send GET request to /activities
        Assert: Verify participants list matches expected data
        """
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        chess_club_participants = activities["Chess Club"]["participants"]
        assert len(chess_club_participants) == 2
        assert "michael@mergington.edu" in chess_club_participants
        assert "daniel@mergington.edu" in chess_club_participants
