"""
Test suite for Article Scraper API endpoints
Tests: /api/scraper/from-url, /api/scraper/save, /api/scraper/discover
"""
import pytest
import requests
import os
import uuid

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL')
if BASE_URL:
    BASE_URL = BASE_URL.rstrip('/')


class TestScraperDiscover:
    """Tests for /api/scraper/discover endpoint - discover article URLs from sources"""
    
    def test_discover_tecmint_urls(self):
        """Test discover endpoint with tecmint source"""
        response = requests.post(f"{BASE_URL}/api/scraper/discover?source=tecmint")
        assert response.status_code == 200
        data = response.json()
        assert data["source"] == "tecmint"
        assert "urls" in data
        assert isinstance(data["urls"], list)
        assert len(data["urls"]) > 0
        assert data["count"] == len(data["urls"])
        assert "available_sources" in data
        print(f"PASS: Discover tecmint returned {data['count']} URLs")
    
    def test_discover_linuxize_urls(self):
        """Test discover endpoint with linuxize source"""
        response = requests.post(f"{BASE_URL}/api/scraper/discover?source=linuxize")
        assert response.status_code == 200
        data = response.json()
        assert data["source"] == "linuxize"
        assert "urls" in data
        assert isinstance(data["urls"], list)
        assert len(data["urls"]) > 0
        print(f"PASS: Discover linuxize returned {data['count']} URLs")
    
    def test_discover_digitalocean_urls(self):
        """Test discover endpoint with digitalocean source"""
        response = requests.post(f"{BASE_URL}/api/scraper/discover?source=digitalocean")
        assert response.status_code == 200
        data = response.json()
        assert data["source"] == "digitalocean"
        assert "urls" in data
        assert isinstance(data["urls"], list)
        assert len(data["urls"]) > 0
        print(f"PASS: Discover digitalocean returned {data['count']} URLs")
    
    def test_discover_default_source(self):
        """Test discover endpoint with default source (linuxize)"""
        response = requests.post(f"{BASE_URL}/api/scraper/discover")
        assert response.status_code == 200
        data = response.json()
        assert data["source"] == "linuxize"  # default
        print(f"PASS: Discover default source returned {data['count']} URLs")
    
    def test_discover_invalid_source_fallback(self):
        """Test discover endpoint with invalid source falls back to linuxize"""
        response = requests.post(f"{BASE_URL}/api/scraper/discover?source=invalid_source")
        assert response.status_code == 200
        data = response.json()
        # Should fallback to linuxize
        assert "urls" in data
        assert len(data["urls"]) > 0
        print(f"PASS: Discover invalid source fallback returned {data['count']} URLs")


class TestScraperFromUrl:
    """Tests for /api/scraper/from-url endpoint - scrape article from URL"""
    
    def test_scrape_tecmint_url(self):
        """Test scraping a tecmint article URL"""
        response = requests.post(
            f"{BASE_URL}/api/scraper/from-url",
            json={"url": "https://www.tecmint.com/install-docker-on-ubuntu/"}
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify article structure
        assert "article" in data
        article = data["article"]
        assert "title" in article
        assert len(article["title"]) > 0
        assert "description" in article
        assert "category" in article
        assert "difficulty" in article
        assert "os" in article
        assert isinstance(article["os"], list)
        assert "tags" in article
        assert isinstance(article["tags"], list)
        assert "steps" in article
        assert isinstance(article["steps"], list)
        assert article["steps_count"] > 0
        assert "source_url" in article
        
        # Verify full_article for saving
        assert "full_article" in data
        assert "is_duplicate" in data
        
        print(f"PASS: Scraped '{article['title']}' with {article['steps_count']} steps")
    
    def test_scrape_url_returns_steps_with_code(self):
        """Test that scraped article has steps with code blocks"""
        response = requests.post(
            f"{BASE_URL}/api/scraper/from-url",
            json={"url": "https://www.tecmint.com/install-docker-on-ubuntu/"}
        )
        assert response.status_code == 200
        data = response.json()
        
        steps = data["article"]["steps"]
        assert len(steps) > 0
        
        # Check step structure
        for step in steps:
            assert "title" in step
            assert "code" in step
            assert "language" in step
        
        print(f"PASS: Steps have proper structure with code blocks")
    
    def test_scrape_empty_url(self):
        """Test scraping with empty URL returns error"""
        response = requests.post(
            f"{BASE_URL}/api/scraper/from-url",
            json={"url": ""}
        )
        # Should return 400 or 422 for validation error
        assert response.status_code in [400, 422]
        print(f"PASS: Empty URL returns {response.status_code}")
    
    def test_scrape_invalid_url(self):
        """Test scraping with invalid URL returns error"""
        response = requests.post(
            f"{BASE_URL}/api/scraper/from-url",
            json={"url": "not-a-valid-url"}
        )
        assert response.status_code == 400
        print(f"PASS: Invalid URL returns 400")
    
    def test_scrape_nonexistent_url(self):
        """Test scraping with non-existent URL returns error"""
        response = requests.post(
            f"{BASE_URL}/api/scraper/from-url",
            json={"url": "https://www.tecmint.com/this-page-does-not-exist-12345/"}
        )
        assert response.status_code == 400
        print(f"PASS: Non-existent URL returns 400")


class TestScraperSave:
    """Tests for /api/scraper/save endpoint - save scraped article to DB"""
    
    def test_save_scraped_article(self):
        """Test saving a scraped article to database"""
        # First scrape an article
        scrape_response = requests.post(
            f"{BASE_URL}/api/scraper/from-url",
            json={"url": "https://www.tecmint.com/install-docker-on-ubuntu/"}
        )
        assert scrape_response.status_code == 200
        scraped_data = scrape_response.json()
        
        # Modify title to make it unique for testing
        article = scraped_data["full_article"]
        unique_title = f"TEST_Scraper_{uuid.uuid4().hex[:8]}_{article['title']}"
        article["title"] = unique_title
        
        # Save the article
        save_response = requests.post(
            f"{BASE_URL}/api/scraper/save",
            json=article
        )
        assert save_response.status_code == 200
        save_data = save_response.json()
        assert "message" in save_data
        assert "slug" in save_data
        print(f"PASS: Saved article with slug '{save_data['slug']}'")
    
    def test_save_article_without_title(self):
        """Test saving article without title returns error"""
        response = requests.post(
            f"{BASE_URL}/api/scraper/save",
            json={"steps": [{"title": "Step 1", "code": "echo test", "language": "bash"}]}
        )
        assert response.status_code == 400
        print(f"PASS: Save without title returns 400")
    
    def test_save_article_without_steps(self):
        """Test saving article without steps returns error"""
        response = requests.post(
            f"{BASE_URL}/api/scraper/save",
            json={"title": "Test Article Without Steps"}
        )
        assert response.status_code == 400
        print(f"PASS: Save without steps returns 400")
    
    def test_save_duplicate_article(self):
        """Test saving duplicate article returns 409 conflict"""
        # First scrape and save an article
        scrape_response = requests.post(
            f"{BASE_URL}/api/scraper/from-url",
            json={"url": "https://www.tecmint.com/install-docker-on-ubuntu/"}
        )
        assert scrape_response.status_code == 200
        scraped_data = scrape_response.json()
        
        # Create unique title
        article = scraped_data["full_article"]
        unique_title = f"TEST_Duplicate_{uuid.uuid4().hex[:8]}"
        article["title"] = unique_title
        
        # Save first time
        save_response1 = requests.post(
            f"{BASE_URL}/api/scraper/save",
            json=article
        )
        assert save_response1.status_code == 200
        
        # Try to save again with same title
        save_response2 = requests.post(
            f"{BASE_URL}/api/scraper/save",
            json=article
        )
        assert save_response2.status_code == 409
        print(f"PASS: Duplicate article returns 409 conflict")


class TestScraperIntegration:
    """Integration tests for full scraper workflow"""
    
    def test_full_scrape_and_save_workflow(self):
        """Test complete workflow: discover -> scrape -> save"""
        # Step 1: Discover URLs
        discover_response = requests.post(f"{BASE_URL}/api/scraper/discover?source=tecmint")
        assert discover_response.status_code == 200
        urls = discover_response.json()["urls"]
        assert len(urls) > 0
        
        # Step 2: Scrape first URL
        scrape_response = requests.post(
            f"{BASE_URL}/api/scraper/from-url",
            json={"url": urls[0]}
        )
        assert scrape_response.status_code == 200
        scraped_data = scrape_response.json()
        
        # Step 3: Modify and save
        article = scraped_data["full_article"]
        article["title"] = f"TEST_Workflow_{uuid.uuid4().hex[:8]}_{article['title']}"
        
        save_response = requests.post(
            f"{BASE_URL}/api/scraper/save",
            json=article
        )
        assert save_response.status_code == 200
        
        print(f"PASS: Full workflow completed - discovered, scraped, and saved article")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
