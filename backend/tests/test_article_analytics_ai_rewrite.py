"""
Test suite for Per-Article Analytics and AI Rewrite features
Tests: article-analytics endpoints, ai-rewrite endpoint
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestArticleAnalyticsOverview:
    """Tests for GET /api/article-analytics/overview"""
    
    def test_overview_returns_expected_fields(self):
        """Overview should return total_articles, total_views, total_likes, avg_views, zero_view_articles, top_viewed, top_liked"""
        response = requests.get(f"{BASE_URL}/api/article-analytics/overview")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        # Check all required fields exist
        assert "total_articles" in data, "Missing total_articles"
        assert "total_views" in data, "Missing total_views"
        assert "total_likes" in data, "Missing total_likes"
        assert "avg_views" in data, "Missing avg_views"
        assert "zero_view_articles" in data, "Missing zero_view_articles"
        assert "top_viewed" in data, "Missing top_viewed"
        assert "top_liked" in data, "Missing top_liked"
        
        # Validate types
        assert isinstance(data["total_articles"], int)
        assert isinstance(data["total_views"], int)
        assert isinstance(data["total_likes"], int)
        assert isinstance(data["avg_views"], (int, float))
        assert isinstance(data["zero_view_articles"], int)
        assert isinstance(data["top_viewed"], list)
        assert isinstance(data["top_liked"], list)
        
        print(f"Overview: {data['total_articles']} articles, {data['total_views']} views, {data['total_likes']} likes")


class TestArticleAnalyticsTopArticles:
    """Tests for GET /api/article-analytics/top-articles"""
    
    def test_top_articles_default(self):
        """Top articles should return list with default limit"""
        response = requests.get(f"{BASE_URL}/api/article-analytics/top-articles")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        print(f"Top articles returned: {len(data)} articles")
    
    def test_top_articles_with_limit(self):
        """Top articles should respect limit parameter"""
        response = requests.get(f"{BASE_URL}/api/article-analytics/top-articles?limit=5")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 5
        print(f"Top 5 articles: {len(data)} returned")
    
    def test_top_articles_sorted_by_views(self):
        """Top articles sorted by views should be in descending order"""
        response = requests.get(f"{BASE_URL}/api/article-analytics/top-articles?limit=5&sort_by=views")
        assert response.status_code == 200
        
        data = response.json()
        if len(data) >= 2:
            # Check descending order
            for i in range(len(data) - 1):
                assert data[i].get("views", 0) >= data[i+1].get("views", 0), "Not sorted by views descending"
        
        # Check article structure
        if data:
            article = data[0]
            assert "title" in article
            assert "slug" in article
            assert "views" in article
            print(f"Top by views: {article['title']} ({article['views']} views)")
    
    def test_top_articles_sorted_by_likes(self):
        """Top articles sorted by likes should be in descending order"""
        response = requests.get(f"{BASE_URL}/api/article-analytics/top-articles?limit=5&sort_by=likes")
        assert response.status_code == 200
        
        data = response.json()
        if len(data) >= 2:
            for i in range(len(data) - 1):
                assert data[i].get("likes", 0) >= data[i+1].get("likes", 0), "Not sorted by likes descending"
        
        if data:
            article = data[0]
            print(f"Top by likes: {article['title']} ({article.get('likes', 0)} likes)")


class TestArticleAnalyticsCategoryStats:
    """Tests for GET /api/article-analytics/category-stats"""
    
    def test_category_stats_returns_list(self):
        """Category stats should return list of categories with stats"""
        response = requests.get(f"{BASE_URL}/api/article-analytics/category-stats")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        
        if data:
            cat = data[0]
            assert "category" in cat
            assert "count" in cat
            assert "total_views" in cat
            assert "total_likes" in cat
            assert "avg_views" in cat
            assert "avg_likes" in cat
            print(f"Category stats: {len(data)} categories, top: {cat['category']} ({cat['count']} articles)")


class TestArticleAnalyticsArticleDetail:
    """Tests for GET /api/article-analytics/article/{slug}"""
    
    def test_article_detail_with_valid_slug(self):
        """Article detail should return engagement_rate, steps_count, total_code_lines"""
        # First get a valid slug from top articles
        top_resp = requests.get(f"{BASE_URL}/api/article-analytics/top-articles?limit=1")
        assert top_resp.status_code == 200
        
        articles = top_resp.json()
        if not articles:
            pytest.skip("No articles in database to test")
        
        slug = articles[0]["slug"]
        
        # Now get article detail
        response = requests.get(f"{BASE_URL}/api/article-analytics/article/{slug}")
        assert response.status_code == 200
        
        data = response.json()
        assert "title" in data
        assert "slug" in data
        assert "engagement_rate" in data
        assert "steps_count" in data
        assert "total_code_lines" in data
        
        assert isinstance(data["engagement_rate"], (int, float))
        assert isinstance(data["steps_count"], int)
        assert isinstance(data["total_code_lines"], int)
        
        print(f"Article detail: {data['title']} - {data['steps_count']} steps, {data['total_code_lines']} code lines, {data['engagement_rate']}% engagement")
    
    def test_article_detail_with_invalid_slug(self):
        """Article detail with invalid slug should return 404"""
        response = requests.get(f"{BASE_URL}/api/article-analytics/article/nonexistent-slug-12345")
        assert response.status_code == 404


class TestAIRewrite:
    """Tests for POST /api/ai-rewrite/rewrite"""
    
    def test_ai_rewrite_endpoint_exists(self):
        """AI rewrite endpoint should exist and accept POST"""
        payload = {
            "title": "Test Article",
            "description": "Test description",
            "steps": [
                {"title": "Step 1", "description": "Do something", "code": "echo hello", "language": "bash"}
            ]
        }
        response = requests.post(f"{BASE_URL}/api/ai-rewrite/rewrite", json=payload)
        
        # Accept 200 (success), 402 (balance low), or 500 (AI error)
        # 402 is expected if EMERGENT_LLM_KEY has no balance
        assert response.status_code in [200, 402, 500], f"Unexpected status: {response.status_code}: {response.text}"
        
        if response.status_code == 200:
            data = response.json()
            assert "rewritten" in data
            assert "original_title" in data
            print(f"AI Rewrite SUCCESS: {data['rewritten'].get('title', 'N/A')}")
        elif response.status_code == 402:
            print("AI Rewrite: 402 - LLM key balance low (expected)")
        else:
            print(f"AI Rewrite: {response.status_code} - {response.json().get('detail', 'Unknown error')}")
    
    def test_ai_rewrite_missing_title(self):
        """AI rewrite should fail with missing title"""
        payload = {
            "description": "Test description",
            "steps": []
        }
        response = requests.post(f"{BASE_URL}/api/ai-rewrite/rewrite", json=payload)
        assert response.status_code == 422, "Should fail validation without title"
    
    def test_ai_rewrite_missing_steps(self):
        """AI rewrite should fail with missing steps"""
        payload = {
            "title": "Test",
            "description": "Test"
        }
        response = requests.post(f"{BASE_URL}/api/ai-rewrite/rewrite", json=payload)
        assert response.status_code == 422, "Should fail validation without steps"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
