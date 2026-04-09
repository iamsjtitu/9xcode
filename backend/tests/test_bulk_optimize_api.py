"""
Test Bulk Optimize API endpoints
- GET /api/ai-rewrite/articles-for-optimize - List articles with optimization status
- POST /api/ai-rewrite/optimize-existing - Optimize a single article (tested with validation only)
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestArticlesForOptimize:
    """Test GET /api/ai-rewrite/articles-for-optimize endpoint"""
    
    def test_articles_for_optimize_basic(self):
        """Test basic endpoint returns paginated articles"""
        response = requests.get(f"{BASE_URL}/api/ai-rewrite/articles-for-optimize")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        # Verify response structure
        assert "articles" in data, "Response should have 'articles' key"
        assert "total" in data, "Response should have 'total' key"
        assert "page" in data, "Response should have 'page' key"
        assert "pages" in data, "Response should have 'pages' key"
        assert "categories" in data, "Response should have 'categories' key"
        assert "optimized_count" in data, "Response should have 'optimized_count' key"
        assert "total_articles" in data, "Response should have 'total_articles' key"
        
        # Verify data types
        assert isinstance(data["articles"], list), "articles should be a list"
        assert isinstance(data["total"], int), "total should be an integer"
        assert isinstance(data["page"], int), "page should be an integer"
        assert isinstance(data["pages"], int), "pages should be an integer"
        assert isinstance(data["categories"], list), "categories should be a list"
        assert isinstance(data["optimized_count"], int), "optimized_count should be an integer"
        assert isinstance(data["total_articles"], int), "total_articles should be an integer"
        
        print(f"✓ Basic endpoint works - Total: {data['total_articles']}, Optimized: {data['optimized_count']}")
    
    def test_articles_for_optimize_pagination(self):
        """Test pagination parameters"""
        # Test page 1 with limit 10
        response = requests.get(f"{BASE_URL}/api/ai-rewrite/articles-for-optimize?page=1&limit=10")
        assert response.status_code == 200
        
        data = response.json()
        assert data["page"] == 1, "Page should be 1"
        assert len(data["articles"]) <= 10, "Should return at most 10 articles"
        
        # Test page 2
        if data["pages"] > 1:
            response2 = requests.get(f"{BASE_URL}/api/ai-rewrite/articles-for-optimize?page=2&limit=10")
            assert response2.status_code == 200
            data2 = response2.json()
            assert data2["page"] == 2, "Page should be 2"
            
            # Verify different articles on different pages
            if len(data["articles"]) > 0 and len(data2["articles"]) > 0:
                slugs_page1 = {a["slug"] for a in data["articles"]}
                slugs_page2 = {a["slug"] for a in data2["articles"]}
                assert slugs_page1.isdisjoint(slugs_page2), "Pages should have different articles"
        
        print(f"✓ Pagination works - Page 1 has {len(data['articles'])} articles, Total pages: {data['pages']}")
    
    def test_articles_for_optimize_category_filter(self):
        """Test category filter parameter"""
        # First get available categories
        response = requests.get(f"{BASE_URL}/api/ai-rewrite/articles-for-optimize")
        assert response.status_code == 200
        data = response.json()
        
        if len(data["categories"]) > 0:
            test_category = data["categories"][0]
            
            # Filter by category
            response2 = requests.get(f"{BASE_URL}/api/ai-rewrite/articles-for-optimize?category={test_category}")
            assert response2.status_code == 200
            data2 = response2.json()
            
            # Verify all returned articles have the correct category
            for article in data2["articles"]:
                assert article.get("category") == test_category, f"Article should have category '{test_category}'"
            
            print(f"✓ Category filter works - Filtered by '{test_category}', got {len(data2['articles'])} articles")
        else:
            print("⚠ No categories available to test filter")
    
    def test_articles_for_optimize_status_filter_pending(self):
        """Test filter_status=pending parameter"""
        response = requests.get(f"{BASE_URL}/api/ai-rewrite/articles-for-optimize?filter_status=pending")
        assert response.status_code == 200
        
        data = response.json()
        # Verify all returned articles are NOT optimized
        for article in data["articles"]:
            assert article.get("ai_optimized") != True, "Pending articles should not be ai_optimized=True"
        
        print(f"✓ Pending filter works - Got {len(data['articles'])} pending articles")
    
    def test_articles_for_optimize_status_filter_optimized(self):
        """Test filter_status=optimized parameter"""
        response = requests.get(f"{BASE_URL}/api/ai-rewrite/articles-for-optimize?filter_status=optimized")
        assert response.status_code == 200
        
        data = response.json()
        # Verify all returned articles ARE optimized
        for article in data["articles"]:
            assert article.get("ai_optimized") == True, "Optimized articles should have ai_optimized=True"
        
        print(f"✓ Optimized filter works - Got {len(data['articles'])} optimized articles")
    
    def test_articles_for_optimize_article_structure(self):
        """Test that articles have correct fields"""
        response = requests.get(f"{BASE_URL}/api/ai-rewrite/articles-for-optimize?limit=5")
        assert response.status_code == 200
        
        data = response.json()
        if len(data["articles"]) > 0:
            article = data["articles"][0]
            
            # Verify required fields
            assert "slug" in article, "Article should have 'slug'"
            assert "title" in article, "Article should have 'title'"
            assert "category" in article, "Article should have 'category'"
            
            # Verify _id is excluded
            assert "_id" not in article, "Article should NOT have '_id' (MongoDB ObjectId)"
            
            print(f"✓ Article structure correct - Sample: {article.get('title', 'N/A')[:50]}...")
        else:
            print("⚠ No articles to verify structure")
    
    def test_articles_for_optimize_combined_filters(self):
        """Test combining category and status filters"""
        # Get categories first
        response = requests.get(f"{BASE_URL}/api/ai-rewrite/articles-for-optimize")
        assert response.status_code == 200
        data = response.json()
        
        if len(data["categories"]) > 0:
            test_category = data["categories"][0]
            
            # Filter by both category and pending status
            response2 = requests.get(
                f"{BASE_URL}/api/ai-rewrite/articles-for-optimize?category={test_category}&filter_status=pending"
            )
            assert response2.status_code == 200
            data2 = response2.json()
            
            # Verify all articles match both filters
            for article in data2["articles"]:
                assert article.get("category") == test_category, f"Article should have category '{test_category}'"
                assert article.get("ai_optimized") != True, "Article should be pending (not optimized)"
            
            print(f"✓ Combined filters work - Category '{test_category}' + Pending: {len(data2['articles'])} articles")
        else:
            print("⚠ No categories available to test combined filters")


class TestOptimizeExisting:
    """Test POST /api/ai-rewrite/optimize-existing endpoint (validation only)"""
    
    def test_optimize_existing_missing_slug(self):
        """Test that missing slug returns 422"""
        response = requests.post(
            f"{BASE_URL}/api/ai-rewrite/optimize-existing",
            json={}
        )
        assert response.status_code == 422, f"Expected 422 for missing slug, got {response.status_code}"
        print("✓ Missing slug returns 422")
    
    def test_optimize_existing_invalid_slug(self):
        """Test that non-existent slug returns 404"""
        response = requests.post(
            f"{BASE_URL}/api/ai-rewrite/optimize-existing",
            json={"slug": "this-slug-definitely-does-not-exist-12345"}
        )
        assert response.status_code == 404, f"Expected 404 for invalid slug, got {response.status_code}"
        
        data = response.json()
        assert "detail" in data, "Response should have error detail"
        print("✓ Invalid slug returns 404")
    
    def test_optimize_existing_valid_slug_structure(self):
        """Test that valid slug is accepted (may fail due to LLM key but validates structure)"""
        # Get a real article slug first
        response = requests.get(f"{BASE_URL}/api/ai-rewrite/articles-for-optimize?limit=1")
        assert response.status_code == 200
        data = response.json()
        
        if len(data["articles"]) > 0:
            test_slug = data["articles"][0]["slug"]
            
            # Try to optimize - may fail due to LLM key but should not be 422 or 404
            response2 = requests.post(
                f"{BASE_URL}/api/ai-rewrite/optimize-existing",
                json={"slug": test_slug}
            )
            
            # Should NOT be 422 (validation error) or 404 (not found)
            # May be 500 (LLM error) or 402 (balance low) or 200 (success)
            assert response2.status_code not in [422, 404], \
                f"Valid slug should not return 422 or 404, got {response2.status_code}"
            
            print(f"✓ Valid slug '{test_slug}' accepted - Status: {response2.status_code}")
        else:
            pytest.skip("No articles available to test optimize-existing")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
