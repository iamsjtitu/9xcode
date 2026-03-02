"""
Test suite for:
- About/Contact/Contribute pages API endpoints
- Contributions submission and management (approve/reject)
- Contact form submission
"""
import pytest
import requests
import os
import uuid

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')


class TestContactAPI:
    """Contact form endpoint tests"""

    def test_contact_submit_success(self):
        """Test successful contact message submission"""
        response = requests.post(f"{BASE_URL}/api/contact", json={
            "name": f"TEST_User_{uuid.uuid4().hex[:6]}",
            "email": "testuser@example.com",
            "subject": "Test Inquiry",
            "message": "This is a test message for contact form"
        })
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        assert "message" in data
        assert data["message"] == "Message sent successfully!"

    def test_contact_submit_missing_name(self):
        """Test contact submission fails without name"""
        response = requests.post(f"{BASE_URL}/api/contact", json={
            "name": "",
            "email": "testuser@example.com",
            "subject": "Test",
            "message": "Test message"
        })
        assert response.status_code == 400

    def test_contact_submit_missing_email(self):
        """Test contact submission fails without email"""
        response = requests.post(f"{BASE_URL}/api/contact", json={
            "name": "Test User",
            "email": "",
            "subject": "Test",
            "message": "Test message"
        })
        assert response.status_code == 400


class TestContributionsAPI:
    """Contributions CRUD endpoint tests"""

    def test_contribution_submit_success(self):
        """Test successful contribution submission"""
        unique_title = f"TEST_Contribution_{uuid.uuid4().hex[:8]}"
        response = requests.post(f"{BASE_URL}/api/contributions/submit", json={
            "contributorName": "Test Contributor",
            "contributorEmail": "contributor@example.com",
            "title": unique_title,
            "description": "A test tutorial about testing APIs",
            "category": "installation",
            "difficulty": "beginner",
            "os": ["ubuntu", "debian"],
            "tags": ["test", "api", "automation"],
            "steps": [
                {
                    "title": "Step 1: Setup",
                    "description": "First step description",
                    "code": "echo 'Hello World'",
                    "language": "bash"
                }
            ]
        })
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        assert "message" in data
        assert "id" in data
        assert data["message"] == "Article submitted for review!"
        return data["id"]

    def test_contribution_submit_missing_contributor_info(self):
        """Test contribution fails without contributor info"""
        response = requests.post(f"{BASE_URL}/api/contributions/submit", json={
            "contributorName": "",
            "contributorEmail": "",
            "title": "Test Article",
            "description": "Test description",
            "category": "installation",
            "steps": [{"title": "Step1", "code": "echo test", "language": "bash"}]
        })
        assert response.status_code == 400

    def test_contribution_submit_missing_steps(self):
        """Test contribution fails without steps"""
        response = requests.post(f"{BASE_URL}/api/contributions/submit", json={
            "contributorName": "Tester",
            "contributorEmail": "tester@example.com",
            "title": "Test Article",
            "description": "Test description",
            "category": "installation",
            "steps": []
        })
        assert response.status_code == 400

    def test_contributions_list_pending(self):
        """Test listing pending contributions"""
        response = requests.get(f"{BASE_URL}/api/contributions?status=pending")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        assert "contributions" in data
        assert "total" in data
        assert "page" in data
        assert "pages" in data
        assert isinstance(data["contributions"], list)

    def test_contributions_list_approved(self):
        """Test listing approved contributions"""
        response = requests.get(f"{BASE_URL}/api/contributions?status=approved")
        assert response.status_code == 200
        data = response.json()
        assert "contributions" in data
        assert isinstance(data["contributions"], list)

    def test_contributions_list_rejected(self):
        """Test listing rejected contributions"""
        response = requests.get(f"{BASE_URL}/api/contributions?status=rejected")
        assert response.status_code == 200
        data = response.json()
        assert "contributions" in data
        assert isinstance(data["contributions"], list)

    def test_contribution_pending_count(self):
        """Test pending count endpoint"""
        response = requests.get(f"{BASE_URL}/api/contributions/pending-count")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        assert "count" in data
        assert isinstance(data["count"], int)


class TestContributionWorkflow:
    """Test the full contribution workflow: submit -> approve/reject"""

    def test_submit_and_approve_contribution(self):
        """Test submitting a contribution and approving it"""
        # Submit a new contribution
        unique_title = f"TEST_Approve_{uuid.uuid4().hex[:8]}"
        submit_response = requests.post(f"{BASE_URL}/api/contributions/submit", json={
            "contributorName": "Approve Tester",
            "contributorEmail": "approve@example.com",
            "title": unique_title,
            "description": "This contribution will be approved",
            "category": "security",
            "difficulty": "intermediate",
            "os": ["ubuntu"],
            "tags": ["test", "approval"],
            "steps": [
                {
                    "title": "Step 1",
                    "description": "Do something",
                    "code": "sudo apt update",
                    "language": "bash"
                }
            ]
        })
        assert submit_response.status_code == 200
        contribution_id = submit_response.json()["id"]

        # Approve the contribution
        approve_response = requests.post(f"{BASE_URL}/api/contributions/{contribution_id}/approve")
        assert approve_response.status_code == 200, f"Expected 200, got {approve_response.status_code}: {approve_response.text}"
        approve_data = approve_response.json()
        assert "message" in approve_data
        assert "approved" in approve_data["message"].lower() or "published" in approve_data["message"].lower()

        # Verify contribution status changed
        list_response = requests.get(f"{BASE_URL}/api/contributions?status=approved")
        assert list_response.status_code == 200

    def test_submit_and_reject_contribution(self):
        """Test submitting a contribution and rejecting it"""
        # Submit a new contribution
        unique_title = f"TEST_Reject_{uuid.uuid4().hex[:8]}"
        submit_response = requests.post(f"{BASE_URL}/api/contributions/submit", json={
            "contributorName": "Reject Tester",
            "contributorEmail": "reject@example.com",
            "title": unique_title,
            "description": "This contribution will be rejected",
            "category": "networking",
            "difficulty": "beginner",
            "os": ["centos"],
            "tags": ["test", "rejection"],
            "steps": [
                {
                    "title": "Step 1",
                    "description": "Network test",
                    "code": "ping localhost",
                    "language": "bash"
                }
            ]
        })
        assert submit_response.status_code == 200
        contribution_id = submit_response.json()["id"]

        # Reject the contribution
        reject_response = requests.post(f"{BASE_URL}/api/contributions/{contribution_id}/reject")
        assert reject_response.status_code == 200, f"Expected 200, got {reject_response.status_code}: {reject_response.text}"
        reject_data = reject_response.json()
        assert "message" in reject_data
        assert "rejected" in reject_data["message"].lower()

    def test_approve_nonexistent_contribution(self):
        """Test approving a non-existent contribution returns 404"""
        fake_id = str(uuid.uuid4())
        response = requests.post(f"{BASE_URL}/api/contributions/{fake_id}/approve")
        assert response.status_code == 404

    def test_reject_nonexistent_contribution(self):
        """Test rejecting a non-existent contribution returns 404"""
        fake_id = str(uuid.uuid4())
        response = requests.post(f"{BASE_URL}/api/contributions/{fake_id}/reject")
        assert response.status_code == 404


class TestExistingContribution:
    """Test with the existing pending contribution mentioned in the test request"""

    def test_check_existing_contribution(self):
        """Check if the existing contribution is accessible"""
        # ID from test request: 1529ca7b-899c-4b28-965b-2a92d0469d19
        existing_id = "1529ca7b-899c-4b28-965b-2a92d0469d19"
        
        # List pending contributions to check if it exists
        response = requests.get(f"{BASE_URL}/api/contributions?status=pending&limit=50")
        assert response.status_code == 200
        data = response.json()
        
        # Check if our contribution exists in the list
        contribution_ids = [c["id"] for c in data["contributions"]]
        if existing_id in contribution_ids:
            print(f"Found existing contribution: {existing_id}")
        else:
            print(f"Existing contribution {existing_id} not found in pending list (may have been approved/rejected already)")


class TestLoginAPI:
    """Test admin login API"""

    def test_login_success(self):
        """Test successful admin login"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "username": "admin",
            "password": "admin123"
        })
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        assert "access_token" in data

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "username": "wronguser",
            "password": "wrongpassword"
        })
        assert response.status_code == 401


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
