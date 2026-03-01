"""
Tests for 9xCodes Newsletter and Bulk Article Management APIs
Features: Newsletter subscription, Subscribers management, Bulk article operations, Export
"""

import pytest
import requests
import os
import uuid

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')
API_URL = f"{BASE_URL}/api"

# Generate unique test emails to avoid conflicts
TEST_EMAIL_PREFIX = f"test_{uuid.uuid4().hex[:8]}"


class TestNewsletterSubscribe:
    """Tests for POST /api/newsletter/subscribe endpoint"""

    def test_subscribe_success(self):
        """Subscribe with valid email returns success"""
        test_email = f"{TEST_EMAIL_PREFIX}_sub1@9xcodes.com"
        response = requests.post(f"{API_URL}/newsletter/subscribe", json={"email": test_email})
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["email"] == test_email.lower()
        print(f"✓ Subscribed successfully: {test_email}")

    def test_subscribe_duplicate_returns_409(self):
        """Subscribing same email twice returns 409 conflict"""
        test_email = f"{TEST_EMAIL_PREFIX}_dup@9xcodes.com"
        # First subscription
        response1 = requests.post(f"{API_URL}/newsletter/subscribe", json={"email": test_email})
        assert response1.status_code == 200
        
        # Second subscription - should fail
        response2 = requests.post(f"{API_URL}/newsletter/subscribe", json={"email": test_email})
        assert response2.status_code == 409
        assert "already" in response2.json().get("detail", "").lower()
        print(f"✓ Duplicate subscription correctly returns 409")

    def test_subscribe_invalid_email_returns_400(self):
        """Invalid email format returns 400"""
        response = requests.post(f"{API_URL}/newsletter/subscribe", json={"email": "invalid-email"})
        assert response.status_code == 400
        print("✓ Invalid email correctly returns 400")

    def test_subscribe_empty_email_returns_400(self):
        """Empty email returns 400"""
        response = requests.post(f"{API_URL}/newsletter/subscribe", json={"email": ""})
        assert response.status_code == 400
        print("✓ Empty email correctly returns 400")

    def test_subscribe_normalizes_email_to_lowercase(self):
        """Email is normalized to lowercase"""
        test_email = f"{TEST_EMAIL_PREFIX}_UPPER@9XCODES.COM"
        response = requests.post(f"{API_URL}/newsletter/subscribe", json={"email": test_email})
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_email.lower()
        print(f"✓ Email normalized: {test_email} → {data['email']}")


class TestNewsletterSubscribersList:
    """Tests for GET /api/newsletter/subscribers endpoint"""

    def test_list_subscribers_returns_paginated_results(self):
        """List subscribers returns paginated data"""
        response = requests.get(f"{API_URL}/newsletter/subscribers?page=1&limit=10")
        assert response.status_code == 200
        data = response.json()
        
        assert "subscribers" in data
        assert "total" in data
        assert "page" in data
        assert "pages" in data
        assert isinstance(data["subscribers"], list)
        print(f"✓ Subscribers list: {len(data['subscribers'])} of {data['total']} total")

    def test_list_subscribers_search_filter(self):
        """Search filter works correctly"""
        # Create a test subscriber
        test_email = f"{TEST_EMAIL_PREFIX}_search@9xcodes.com"
        requests.post(f"{API_URL}/newsletter/subscribe", json={"email": test_email})
        
        # Search for it
        response = requests.get(f"{API_URL}/newsletter/subscribers?search={TEST_EMAIL_PREFIX}_search")
        assert response.status_code == 200
        data = response.json()
        
        # Should find the test subscriber
        emails = [s['email'] for s in data['subscribers']]
        assert any(TEST_EMAIL_PREFIX in e for e in emails)
        print(f"✓ Search filter working: found {len(data['subscribers'])} matches")

    def test_list_subscribers_pagination(self):
        """Pagination works correctly"""
        response = requests.get(f"{API_URL}/newsletter/subscribers?page=1&limit=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data["subscribers"]) <= 5
        print(f"✓ Pagination limit=5 returned {len(data['subscribers'])} subscribers")

    def test_list_subscribers_has_required_fields(self):
        """Subscriber objects have required fields"""
        response = requests.get(f"{API_URL}/newsletter/subscribers?limit=1")
        assert response.status_code == 200
        data = response.json()
        
        if len(data["subscribers"]) > 0:
            sub = data["subscribers"][0]
            assert "email" in sub
            assert "subscribedAt" in sub
            print(f"✓ Subscriber has required fields: {sub['email']}")


class TestNewsletterExport:
    """Tests for GET /api/newsletter/subscribers/export endpoint"""

    def test_export_csv_returns_file(self):
        """Export returns CSV file"""
        response = requests.get(f"{API_URL}/newsletter/subscribers/export")
        assert response.status_code == 200
        assert "text/csv" in response.headers.get("Content-Type", "")
        assert "attachment" in response.headers.get("Content-Disposition", "")
        
        # Verify CSV structure
        content = response.text
        lines = content.strip().split("\n")
        assert len(lines) >= 1  # At least header
        assert "Email" in lines[0]
        print(f"✓ CSV export returned {len(lines)-1} subscribers")


class TestNewsletterDelete:
    """Tests for DELETE /api/newsletter/subscribers/{email} endpoint"""

    def test_delete_subscriber_success(self):
        """Delete existing subscriber returns success"""
        # Create a test subscriber
        test_email = f"{TEST_EMAIL_PREFIX}_del@9xcodes.com"
        requests.post(f"{API_URL}/newsletter/subscribe", json={"email": test_email})
        
        # Delete it
        response = requests.delete(f"{API_URL}/newsletter/subscribers/{test_email}")
        assert response.status_code == 200
        assert "removed" in response.json().get("message", "").lower()
        print(f"✓ Deleted subscriber: {test_email}")

    def test_delete_nonexistent_subscriber_returns_404(self):
        """Delete non-existent subscriber returns 404"""
        response = requests.delete(f"{API_URL}/newsletter/subscribers/nonexistent@fake.com")
        assert response.status_code == 404
        print("✓ Delete non-existent subscriber returns 404")


class TestNewsletterCount:
    """Tests for GET /api/newsletter/subscribers/count endpoint"""

    def test_count_returns_total(self):
        """Count endpoint returns total count"""
        response = requests.get(f"{API_URL}/newsletter/subscribers/count")
        assert response.status_code == 200
        data = response.json()
        assert "count" in data
        assert isinstance(data["count"], int)
        print(f"✓ Subscriber count: {data['count']}")


class TestArticlesList:
    """Tests for GET /api/articles/list endpoint"""

    def test_list_articles_returns_paginated_results(self):
        """List articles returns paginated data"""
        response = requests.get(f"{API_URL}/articles/list?page=1&limit=20")
        assert response.status_code == 200
        data = response.json()
        
        assert "articles" in data
        assert "total" in data
        assert "page" in data
        assert "pages" in data
        assert isinstance(data["articles"], list)
        print(f"✓ Articles list: {len(data['articles'])} of {data['total']} total")

    def test_list_articles_category_filter(self):
        """Category filter works correctly"""
        response = requests.get(f"{API_URL}/articles/list?category=installation&limit=10")
        assert response.status_code == 200
        data = response.json()
        
        for article in data["articles"]:
            assert article["category"] == "installation"
        print(f"✓ Category filter working: {len(data['articles'])} installation articles")

    def test_list_articles_search_filter(self):
        """Search filter works correctly"""
        response = requests.get(f"{API_URL}/articles/list?search=nginx&limit=10")
        assert response.status_code == 200
        data = response.json()
        
        # Should find matching articles
        if len(data["articles"]) > 0:
            # Check title or description contains nginx (case insensitive)
            for article in data["articles"]:
                title_match = "nginx" in article.get("title", "").lower()
                desc_match = "nginx" in article.get("description", "").lower()
                assert title_match or desc_match
        print(f"✓ Search filter 'nginx': {len(data['articles'])} results")

    def test_list_articles_has_required_fields(self):
        """Article objects have required fields"""
        response = requests.get(f"{API_URL}/articles/list?limit=1")
        assert response.status_code == 200
        data = response.json()
        
        if len(data["articles"]) > 0:
            article = data["articles"][0]
            required_fields = ["title", "slug", "category", "views", "likes"]
            for field in required_fields:
                assert field in article, f"Missing field: {field}"
            print(f"✓ Article has required fields: {article['title'][:50]}...")


class TestArticlesExport:
    """Tests for GET /api/articles/export endpoint"""

    def test_export_csv_returns_file(self):
        """Export CSV returns valid CSV file"""
        response = requests.get(f"{API_URL}/articles/export?format=csv")
        assert response.status_code == 200
        assert "text/csv" in response.headers.get("Content-Type", "")
        assert "attachment" in response.headers.get("Content-Disposition", "")
        
        # Verify CSV structure
        content = response.text
        lines = content.strip().split("\n")
        assert len(lines) >= 1  # At least header
        assert "Title" in lines[0]
        assert "Slug" in lines[0]
        print(f"✓ CSV export returned {len(lines)-1} articles")

    def test_export_json_returns_file(self):
        """Export JSON returns valid JSON file"""
        response = requests.get(f"{API_URL}/articles/export?format=json")
        assert response.status_code == 200
        assert "application/json" in response.headers.get("Content-Type", "")
        assert "attachment" in response.headers.get("Content-Disposition", "")
        
        # Verify JSON structure
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert "title" in data[0]
            assert "slug" in data[0]
        print(f"✓ JSON export returned {len(data)} articles")


class TestArticlesBulkOperations:
    """Tests for bulk article operations - using careful test approach"""

    def test_bulk_delete_empty_returns_400(self):
        """Bulk delete with empty list returns 400"""
        response = requests.post(f"{API_URL}/articles/bulk-delete", json={"slugs": []})
        assert response.status_code == 400
        print("✓ Bulk delete empty list returns 400")

    def test_bulk_delete_nonexistent_returns_zero_deleted(self):
        """Bulk delete non-existent slugs returns 0 deleted"""
        response = requests.post(f"{API_URL}/articles/bulk-delete", 
                                 json={"slugs": ["nonexistent-slug-12345"]})
        assert response.status_code == 200
        data = response.json()
        assert data["deleted"] == 0
        print("✓ Bulk delete non-existent returns 0 deleted")

    def test_bulk_category_empty_returns_400(self):
        """Bulk category change with empty list returns 400"""
        response = requests.post(f"{API_URL}/articles/bulk-category", 
                                 json={"slugs": [], "category": "security"})
        assert response.status_code == 400
        print("✓ Bulk category empty list returns 400")

    def test_bulk_category_nonexistent_returns_zero_modified(self):
        """Bulk category change for non-existent slugs returns 0 modified"""
        response = requests.post(f"{API_URL}/articles/bulk-category", 
                                 json={"slugs": ["nonexistent-slug-99999"], "category": "security"})
        assert response.status_code == 200
        data = response.json()
        assert data["modified"] == 0
        print("✓ Bulk category non-existent returns 0 modified")


class TestCleanup:
    """Cleanup test data created during tests"""

    def test_cleanup_test_subscribers(self):
        """Remove test subscribers created during tests"""
        # Get all subscribers
        response = requests.get(f"{API_URL}/newsletter/subscribers?limit=200")
        if response.status_code == 200:
            data = response.json()
            for sub in data["subscribers"]:
                if TEST_EMAIL_PREFIX in sub["email"]:
                    requests.delete(f"{API_URL}/newsletter/subscribers/{sub['email']}")
        print(f"✓ Cleaned up test subscribers with prefix: {TEST_EMAIL_PREFIX}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
