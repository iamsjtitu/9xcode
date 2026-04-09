"""
Test AI Rewrite Endpoints
Tests for: /api/ai-rewrite/rewrite, /api/ai-rewrite/seo-optimize, 
           /api/ai-rewrite/summarize, /api/ai-rewrite/full-optimize
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

# Sample test data for AI endpoints
SAMPLE_ARTICLE = {
    "title": "How to Install Nginx on Ubuntu",
    "description": "A comprehensive guide to install Nginx web server on Ubuntu Linux",
    "steps": [
        {
            "title": "Update packages",
            "description": "First update your system packages",
            "code": "sudo apt update && sudo apt upgrade -y",
            "language": "bash"
        },
        {
            "title": "Install Nginx",
            "description": "Install Nginx using apt package manager",
            "code": "sudo apt install nginx -y",
            "language": "bash"
        },
        {
            "title": "Start Nginx service",
            "description": "Start and enable Nginx to run on boot",
            "code": "sudo systemctl start nginx\nsudo systemctl enable nginx",
            "language": "bash"
        }
    ]
}

SAMPLE_SEO_REQUEST = {
    "title": "How to Install Nginx on Ubuntu",
    "description": "A comprehensive guide to install Nginx web server on Ubuntu Linux",
    "category": "web-hosting"
}


class TestAIRewriteEndpoints:
    """Test all AI rewrite endpoints"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test session"""
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    def test_api_health(self):
        """Test API is running"""
        response = self.session.get(f"{BASE_URL}/api/")
        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == "healthy"
        print("✓ API health check passed")
    
    # ===== REWRITE ENDPOINT TESTS =====
    
    def test_rewrite_endpoint_accepts_valid_request(self):
        """Test POST /api/ai-rewrite/rewrite accepts valid data"""
        response = self.session.post(
            f"{BASE_URL}/api/ai-rewrite/rewrite",
            json=SAMPLE_ARTICLE
        )
        # Should return 200 (success) or 402 (low balance) or 500 (AI error)
        # 422 would mean validation failed
        assert response.status_code != 422, f"Validation failed: {response.json()}"
        print(f"✓ Rewrite endpoint responded with status {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            assert "rewritten" in data, "Response should contain 'rewritten' key"
            assert "original_title" in data, "Response should contain 'original_title'"
            print(f"✓ Rewrite returned valid response with rewritten content")
        elif response.status_code == 402:
            print("⚠ LLM key balance low - endpoint works but needs credits")
        elif response.status_code == 500:
            print(f"⚠ AI error: {response.json().get('detail', 'Unknown error')}")
    
    def test_rewrite_missing_title(self):
        """Test rewrite endpoint rejects missing title"""
        invalid_data = {
            "description": "Test description",
            "steps": []
        }
        response = self.session.post(
            f"{BASE_URL}/api/ai-rewrite/rewrite",
            json=invalid_data
        )
        assert response.status_code == 422, "Should return 422 for missing title"
        print("✓ Rewrite correctly rejects missing title")
    
    def test_rewrite_missing_steps(self):
        """Test rewrite endpoint rejects missing steps"""
        invalid_data = {
            "title": "Test Title",
            "description": "Test description"
        }
        response = self.session.post(
            f"{BASE_URL}/api/ai-rewrite/rewrite",
            json=invalid_data
        )
        assert response.status_code == 422, "Should return 422 for missing steps"
        print("✓ Rewrite correctly rejects missing steps")
    
    # ===== SEO OPTIMIZE ENDPOINT TESTS =====
    
    def test_seo_optimize_endpoint_accepts_valid_request(self):
        """Test POST /api/ai-rewrite/seo-optimize accepts valid data"""
        response = self.session.post(
            f"{BASE_URL}/api/ai-rewrite/seo-optimize",
            json=SAMPLE_SEO_REQUEST
        )
        assert response.status_code != 422, f"Validation failed: {response.json()}"
        print(f"✓ SEO optimize endpoint responded with status {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            assert "seo" in data, "Response should contain 'seo' key"
            assert "original_title" in data, "Response should contain 'original_title'"
            seo = data["seo"]
            # Validate SEO response structure
            expected_keys = ["seo_title", "seo_description", "keywords", "tags"]
            for key in expected_keys:
                assert key in seo, f"SEO response should contain '{key}'"
            print(f"✓ SEO optimize returned valid response with metadata")
        elif response.status_code == 402:
            print("⚠ LLM key balance low - endpoint works but needs credits")
        elif response.status_code == 500:
            print(f"⚠ AI error: {response.json().get('detail', 'Unknown error')}")
    
    def test_seo_optimize_missing_title(self):
        """Test SEO optimize endpoint rejects missing title"""
        invalid_data = {
            "description": "Test description"
        }
        response = self.session.post(
            f"{BASE_URL}/api/ai-rewrite/seo-optimize",
            json=invalid_data
        )
        assert response.status_code == 422, "Should return 422 for missing title"
        print("✓ SEO optimize correctly rejects missing title")
    
    def test_seo_optimize_optional_category(self):
        """Test SEO optimize works without category (optional field)"""
        data = {
            "title": "Test Title",
            "description": "Test description"
        }
        response = self.session.post(
            f"{BASE_URL}/api/ai-rewrite/seo-optimize",
            json=data
        )
        # Should not fail validation - category is optional
        assert response.status_code != 422, "Category should be optional"
        print(f"✓ SEO optimize accepts request without category (status: {response.status_code})")
    
    # ===== SUMMARIZE ENDPOINT TESTS =====
    
    def test_summarize_endpoint_accepts_valid_request(self):
        """Test POST /api/ai-rewrite/summarize accepts valid data"""
        response = self.session.post(
            f"{BASE_URL}/api/ai-rewrite/summarize",
            json=SAMPLE_ARTICLE
        )
        assert response.status_code != 422, f"Validation failed: {response.json()}"
        print(f"✓ Summarize endpoint responded with status {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            assert "summary" in data, "Response should contain 'summary' key"
            assert "original_title" in data, "Response should contain 'original_title'"
            summary = data["summary"]
            # Validate summary response structure
            expected_keys = ["description", "summary", "key_takeaways", "difficulty"]
            for key in expected_keys:
                assert key in summary, f"Summary response should contain '{key}'"
            print(f"✓ Summarize returned valid response with summary data")
        elif response.status_code == 402:
            print("⚠ LLM key balance low - endpoint works but needs credits")
        elif response.status_code == 500:
            print(f"⚠ AI error: {response.json().get('detail', 'Unknown error')}")
    
    def test_summarize_missing_title(self):
        """Test summarize endpoint rejects missing title"""
        invalid_data = {
            "description": "Test description",
            "steps": []
        }
        response = self.session.post(
            f"{BASE_URL}/api/ai-rewrite/summarize",
            json=invalid_data
        )
        assert response.status_code == 422, "Should return 422 for missing title"
        print("✓ Summarize correctly rejects missing title")
    
    # ===== FULL OPTIMIZE ENDPOINT TESTS =====
    
    def test_full_optimize_endpoint_accepts_valid_request(self):
        """Test POST /api/ai-rewrite/full-optimize accepts valid data"""
        response = self.session.post(
            f"{BASE_URL}/api/ai-rewrite/full-optimize",
            json=SAMPLE_ARTICLE
        )
        assert response.status_code != 422, f"Validation failed: {response.json()}"
        print(f"✓ Full optimize endpoint responded with status {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            assert "optimized" in data, "Response should contain 'optimized' key"
            assert "original_title" in data, "Response should contain 'original_title'"
            optimized = data["optimized"]
            # Validate full optimize response structure
            expected_keys = ["title", "description", "tags", "difficulty", "steps"]
            for key in expected_keys:
                assert key in optimized, f"Optimized response should contain '{key}'"
            print(f"✓ Full optimize returned valid response with optimized content")
        elif response.status_code == 402:
            print("⚠ LLM key balance low - endpoint works but needs credits")
        elif response.status_code == 500:
            print(f"⚠ AI error: {response.json().get('detail', 'Unknown error')}")
    
    def test_full_optimize_missing_steps(self):
        """Test full optimize endpoint rejects missing steps"""
        invalid_data = {
            "title": "Test Title",
            "description": "Test description"
        }
        response = self.session.post(
            f"{BASE_URL}/api/ai-rewrite/full-optimize",
            json=invalid_data
        )
        assert response.status_code == 422, "Should return 422 for missing steps"
        print("✓ Full optimize correctly rejects missing steps")
    
    # ===== OPTIMIZE EXISTING ENDPOINT TEST =====
    
    def test_optimize_existing_invalid_slug(self):
        """Test optimize-existing returns 404 for invalid slug"""
        response = self.session.post(
            f"{BASE_URL}/api/ai-rewrite/optimize-existing",
            json={"slug": "non-existent-article-slug-12345"}
        )
        assert response.status_code == 404, f"Should return 404 for non-existent slug, got {response.status_code}"
        print("✓ Optimize-existing correctly returns 404 for invalid slug")


class TestScraperEndpoints:
    """Test scraper endpoints that work with AI tools"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test session"""
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    def test_discover_tecmint(self):
        """Test discover endpoint returns URLs for tecmint"""
        response = self.session.post(f"{BASE_URL}/api/scraper/discover?source=tecmint")
        assert response.status_code == 200
        data = response.json()
        assert "urls" in data
        assert "count" in data
        assert data["count"] > 0
        assert data["source"] == "tecmint"
        print(f"✓ Discover returned {data['count']} URLs from tecmint")
    
    def test_discover_phoenixnap(self):
        """Test discover endpoint returns URLs for phoenixnap"""
        response = self.session.post(f"{BASE_URL}/api/scraper/discover?source=phoenixnap")
        assert response.status_code == 200
        data = response.json()
        assert data["source"] == "phoenixnap"
        assert data["count"] > 0
        print(f"✓ Discover returned {data['count']} URLs from phoenixnap")
    
    def test_discover_digitalocean(self):
        """Test discover endpoint returns URLs for digitalocean"""
        response = self.session.post(f"{BASE_URL}/api/scraper/discover?source=digitalocean")
        assert response.status_code == 200
        data = response.json()
        assert data["source"] == "digitalocean"
        assert data["count"] > 0
        print(f"✓ Discover returned {data['count']} URLs from digitalocean")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
