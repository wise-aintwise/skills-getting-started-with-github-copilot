"""Fixtures and test configuration for the Activities API tests."""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def activities_fixture():
    """Provide a fresh copy of test activity data for each test.
    
    This fixture returns a fresh dictionary of activities to ensure
    test isolation and prevent test pollution.
    """
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Join the school soccer team for training and matches",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 22,
            "participants": ["nina@mergington.edu", "alex@mergington.edu"]
        },
        "Basketball Club": {
            "description": "Practice basketball skills and compete in local games",
            "schedule": "Tuesdays and Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["liam@mergington.edu", "sara@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore drawing, painting, and mixed media art projects",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["ava@mergington.edu", "noah@mergington.edu"]
        },
        "Drama Club": {
            "description": "Create and perform plays, improv, and stage productions",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["mia@mergington.edu", "jack@mergington.edu"]
        },
        "Math Olympiad": {
            "description": "Solve challenging math problems and prepare for competitions",
            "schedule": "Mondays, 3:30 PM - 4:30 PM",
            "max_participants": 14,
            "participants": ["isabella@mergington.edu", "ethan@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore science projects together",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["lucas@mergington.edu", "harper@mergington.edu"]
        }
    }


@pytest.fixture
def client(activities_fixture):
    """Provide a TestClient with fresh test data for each test.
    
    Replaces the app's in-memory activities with the fixture data
    to ensure isolation between tests.
    """
    # Replace app's activities with test fixture data
    import src.app
    original_activities = src.app.activities.copy()
    src.app.activities.clear()
    src.app.activities.update(activities_fixture)
    
    # Create test client
    test_client = TestClient(app)
    
    yield test_client
    
    # Restore original activities after test completes
    src.app.activities.clear()
    src.app.activities.update(original_activities)
