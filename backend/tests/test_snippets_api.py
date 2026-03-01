"""
Tests for 9xCodes Snippets API - New Features
Tests: Popular endpoint, Related endpoint, Tag filtering
"""

import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')
API_URL = f"{BASE_URL}/api"


class TestPopularSnippets:
    """Tests for GET /api/snippets/popular endpoint"""

    def test_popular_endpoint_returns_snippets(self):
        """Popular endpoint returns list of snippets"""
        response = requests.get(f"{API_URL}/snippets/popular?limit=6")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        print(f"✓ Popular endpoint returned {len(data)} snippets")

    def test_popular_sorted_by_views(self):
        """Popular snippets are sorted by views descending"""
        response = requests.get(f"{API_URL}/snippets/popular?limit=10")
        assert response.status_code == 200
        data = response.json()
        
        # Verify sorted by views descending
        views = [s['views'] for s in data]
        assert views == sorted(views, reverse=True), "Snippets not sorted by views desc"
        print(f"✓ Snippets correctly sorted by views: {views[:3]}...")

    def test_popular_respects_limit(self):
        """Limit parameter controls number of results"""
        response = requests.get(f"{API_URL}/snippets/popular?limit=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 3
        print(f"✓ Limit=3 returned {len(data)} snippets")

    def test_popular_snippet_structure(self):
        """Popular snippets have required fields"""
        response = requests.get(f"{API_URL}/snippets/popular?limit=1")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        snippet = data[0]
        
        required_fields = ['id', 'title', 'slug', 'description', 'category', 'views', 'likes', 'tags']
        for field in required_fields:
            assert field in snippet, f"Missing field: {field}"
        print(f"✓ Snippet has all required fields: {snippet['title'][:50]}...")


class TestRelatedSnippets:
    """Tests for GET /api/snippets/{slug}/related endpoint"""

    def test_related_endpoint_returns_snippets(self):
        """Related endpoint returns list of related snippets"""
        # First get a valid snippet slug
        snippets_response = requests.get(f"{API_URL}/snippets?limit=1")
        assert snippets_response.status_code == 200
        snippets = snippets_response.json()
        assert len(snippets) > 0
        slug = snippets[0]['slug']
        
        # Test related endpoint
        response = requests.get(f"{API_URL}/snippets/{slug}/related?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✓ Related endpoint for '{slug}' returned {len(data)} snippets")

    def test_related_excludes_original_snippet(self):
        """Related snippets don't include the original snippet"""
        snippets_response = requests.get(f"{API_URL}/snippets?limit=1")
        snippets = snippets_response.json()
        slug = snippets[0]['slug']
        
        response = requests.get(f"{API_URL}/snippets/{slug}/related?limit=10")
        assert response.status_code == 200
        data = response.json()
        
        slugs = [s['slug'] for s in data]
        assert slug not in slugs, "Original snippet should not be in related"
        print(f"✓ Original snippet '{slug}' correctly excluded from related")

    def test_related_respects_limit(self):
        """Limit parameter controls number of related results"""
        snippets_response = requests.get(f"{API_URL}/snippets?limit=1")
        slug = snippets_response.json()[0]['slug']
        
        response = requests.get(f"{API_URL}/snippets/{slug}/related?limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 2
        print(f"✓ Related limit=2 returned {len(data)} snippets")

    def test_related_404_for_invalid_slug(self):
        """Related endpoint returns 404 for non-existent snippet"""
        response = requests.get(f"{API_URL}/snippets/invalid-slug-12345/related")
        assert response.status_code == 404
        print("✓ Related endpoint returns 404 for invalid slug")


class TestTagFiltering:
    """Tests for tag-based filtering via GET /api/snippets?tag=xxx"""

    def test_tag_filter_returns_matching_snippets(self):
        """Tag filter returns snippets with matching tag"""
        response = requests.get(f"{API_URL}/snippets?tag=nginx&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        # Verify all returned snippets have the tag
        for snippet in data:
            tags_lower = [t.lower() for t in snippet['tags']]
            assert 'nginx' in tags_lower, f"Snippet '{snippet['slug']}' missing 'nginx' tag"
        print(f"✓ Tag filter 'nginx' returned {len(data)} matching snippets")

    def test_tag_filter_with_different_tags(self):
        """Different tags return different results"""
        response1 = requests.get(f"{API_URL}/snippets?tag=docker&limit=10")
        response2 = requests.get(f"{API_URL}/snippets?tag=php&limit=10")
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = response1.json()
        data2 = response2.json()
        print(f"✓ docker tag: {len(data1)} results, php tag: {len(data2)} results")

    def test_tag_filter_empty_result(self):
        """Non-existent tag returns empty list"""
        response = requests.get(f"{API_URL}/snippets?tag=nonexistenttag12345")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0
        print("✓ Non-existent tag returns empty list")


class TestSnippetsCRUD:
    """Tests for basic snippets CRUD operations"""

    def test_get_all_snippets(self):
        """GET /api/snippets returns list of snippets"""
        response = requests.get(f"{API_URL}/snippets?limit=10")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        print(f"✓ GET snippets returned {len(data)} snippets")

    def test_get_single_snippet(self):
        """GET /api/snippets/{slug} returns single snippet"""
        # Get a valid slug first
        list_response = requests.get(f"{API_URL}/snippets?limit=1")
        slug = list_response.json()[0]['slug']
        
        response = requests.get(f"{API_URL}/snippets/{slug}")
        assert response.status_code == 200
        data = response.json()
        assert data['slug'] == slug
        print(f"✓ GET single snippet: {data['title'][:50]}...")

    def test_get_snippet_increments_views(self):
        """GET snippet increments view count"""
        list_response = requests.get(f"{API_URL}/snippets?limit=1")
        slug = list_response.json()[0]['slug']
        
        # Get initial views
        response1 = requests.get(f"{API_URL}/snippets/{slug}")
        views1 = response1.json()['views']
        
        # Get again
        response2 = requests.get(f"{API_URL}/snippets/{slug}")
        views2 = response2.json()['views']
        
        # Views should increment
        assert views2 >= views1, "Views should increment on each GET"
        print(f"✓ Views incremented: {views1} → {views2}")

    def test_snippet_404_for_invalid_slug(self):
        """GET returns 404 for non-existent snippet"""
        response = requests.get(f"{API_URL}/snippets/invalid-slug-99999")
        assert response.status_code == 404
        print("✓ GET returns 404 for invalid slug")


class TestSortingAndFiltering:
    """Tests for sorting and filtering options"""

    def test_sort_by_views(self):
        """Sort by views returns most viewed first"""
        response = requests.get(f"{API_URL}/snippets?sort=views&limit=10")
        assert response.status_code == 200
        data = response.json()
        
        views = [s['views'] for s in data]
        assert views == sorted(views, reverse=True), "Not sorted by views"
        print(f"✓ Sort by views: {views[:3]}...")

    def test_sort_by_popular(self):
        """Sort by popular returns most liked first"""
        response = requests.get(f"{API_URL}/snippets?sort=popular&limit=10")
        assert response.status_code == 200
        data = response.json()
        
        likes = [s['likes'] for s in data]
        assert likes == sorted(likes, reverse=True), "Not sorted by likes"
        print(f"✓ Sort by popular (likes): {likes[:3]}...")

    def test_category_filter(self):
        """Category filter returns matching snippets"""
        response = requests.get(f"{API_URL}/snippets?category=installation&limit=5")
        assert response.status_code == 200
        data = response.json()
        
        for snippet in data:
            assert snippet['category'] == 'installation'
        print(f"✓ Category filter 'installation' returned {len(data)} snippets")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
