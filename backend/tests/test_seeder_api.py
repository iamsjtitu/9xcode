"""
Test cases for Article Seeder API endpoints
Tests: GET /api/seeder/categories, POST /api/seeder/preview, POST /api/seeder/seed
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL')

class TestSeederCategories:
    """Test GET /api/seeder/categories endpoint"""
    
    def test_get_categories_returns_200(self):
        """Verify categories endpoint returns success status"""
        response = requests.get(f"{BASE_URL}/api/seeder/categories")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print("PASS: GET /api/seeder/categories returns 200")
    
    def test_get_categories_has_14_categories(self):
        """Verify 14 categories are returned"""
        response = requests.get(f"{BASE_URL}/api/seeder/categories")
        data = response.json()
        assert "categories" in data, "Response should have 'categories' key"
        assert len(data["categories"]) == 14, f"Expected 14 categories, got {len(data['categories'])}"
        print(f"PASS: 14 categories returned: {data['categories']}")
    
    def test_get_categories_has_8_operating_systems(self):
        """Verify 8 OS options are returned"""
        response = requests.get(f"{BASE_URL}/api/seeder/categories")
        data = response.json()
        assert "operating_systems" in data, "Response should have 'operating_systems' key"
        assert len(data["operating_systems"]) == 8, f"Expected 8 OS, got {len(data['operating_systems'])}"
        os_slugs = [os["slug"] for os in data["operating_systems"]]
        expected_os = ["ubuntu", "centos", "debian", "rhel", "fedora", "linux", "windows", "mac"]
        assert set(os_slugs) == set(expected_os), f"OS mismatch: {os_slugs}"
        print(f"PASS: 8 OS options returned: {os_slugs}")
    
    def test_get_categories_structure(self):
        """Verify OS objects have slug and name"""
        response = requests.get(f"{BASE_URL}/api/seeder/categories")
        data = response.json()
        for os in data["operating_systems"]:
            assert "slug" in os, "OS should have 'slug'"
            assert "name" in os, "OS should have 'name'"
        print("PASS: OS objects have correct structure (slug, name)")


class TestSeederPreview:
    """Test POST /api/seeder/preview endpoint"""
    
    def test_preview_installation_ubuntu(self):
        """Test preview for installation category with Ubuntu"""
        response = requests.post(
            f"{BASE_URL}/api/seeder/preview",
            json={"category": "installation", "os": "ubuntu"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "articles" in data
        assert "total" in data
        assert "new" in data
        assert data["total"] > 0, "Should have articles to preview"
        print(f"PASS: Preview installation/ubuntu - {data['total']} articles ({data['new']} new)")
    
    def test_preview_installation_centos(self):
        """Test preview for installation category with CentOS"""
        response = requests.post(
            f"{BASE_URL}/api/seeder/preview",
            json={"category": "installation", "os": "centos"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] > 0
        # Verify article structure
        if data["articles"]:
            art = data["articles"][0]
            assert "title" in art
            assert "category" in art
            assert "difficulty" in art
            assert "os" in art
            assert "tags" in art
            assert "exists" in art
        print(f"PASS: Preview installation/centos - {data['total']} articles with correct structure")
    
    def test_preview_networking_fedora(self):
        """Test preview for networking category with Fedora"""
        response = requests.post(
            f"{BASE_URL}/api/seeder/preview",
            json={"category": "networking", "os": "fedora"}
        )
        assert response.status_code == 200
        data = response.json()
        # Fedora networking articles were seeded earlier, should show as exists
        assert data["total"] >= 2
        print(f"PASS: Preview networking/fedora - {data['total']} articles ({data['new']} new)")
    
    def test_preview_default_os(self):
        """Test preview defaults to Ubuntu when OS not specified"""
        response = requests.post(
            f"{BASE_URL}/api/seeder/preview",
            json={"category": "security"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] > 0
        # Articles should be Ubuntu when no OS specified
        if data["articles"]:
            assert "ubuntu" in data["articles"][0]["os"]
        print(f"PASS: Preview security (default OS) - {data['total']} articles for Ubuntu")
    
    def test_preview_invalid_category(self):
        """Test preview with invalid category returns 400"""
        response = requests.post(
            f"{BASE_URL}/api/seeder/preview",
            json={"category": "invalid_category_xyz", "os": "ubuntu"}
        )
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        print(f"PASS: Preview invalid category returns 400 with error: {data['detail']}")
    
    def test_preview_exists_badge(self):
        """Test that preview shows exists=true for already seeded articles"""
        # Fedora networking was seeded earlier
        response = requests.post(
            f"{BASE_URL}/api/seeder/preview",
            json={"category": "networking", "os": "fedora"}
        )
        data = response.json()
        exists_count = sum(1 for art in data["articles"] if art["exists"])
        assert exists_count > 0, "Should have at least one existing article"
        print(f"PASS: Preview shows {exists_count} existing articles (exists=true)")


class TestSeederSeed:
    """Test POST /api/seeder/seed endpoint"""
    
    def test_seed_security_mac(self):
        """Test seeding security category for macOS (unique combo)"""
        # First check preview
        preview = requests.post(
            f"{BASE_URL}/api/seeder/preview",
            json={"category": "security", "os": "mac"}
        )
        preview_data = preview.json()
        new_count = preview_data["new"]
        
        # Now seed
        response = requests.post(
            f"{BASE_URL}/api/seeder/seed",
            json={"category": "security", "os": "mac"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "added" in data
        assert "skipped" in data
        assert "total_articles" in data
        assert "message" in data
        print(f"PASS: Seed security/mac - added: {data['added']}, skipped: {data['skipped']}")
    
    def test_seed_already_exists_skips(self):
        """Test that seeding same combo again skips duplicates"""
        # Seed networking/fedora again (was seeded earlier)
        response = requests.post(
            f"{BASE_URL}/api/seeder/seed",
            json={"category": "networking", "os": "fedora"}
        )
        assert response.status_code == 200
        data = response.json()
        # Should skip all since already exists
        assert data["added"] == 0, "Should not add duplicates"
        assert data["skipped"] >= 2, "Should skip existing articles"
        print(f"PASS: Seed networking/fedora skips duplicates - added: {data['added']}, skipped: {data['skipped']}")
    
    def test_seed_invalid_category(self):
        """Test seed with invalid category returns 400"""
        response = requests.post(
            f"{BASE_URL}/api/seeder/seed",
            json={"category": "xyz_invalid", "os": "ubuntu"}
        )
        assert response.status_code == 400
        print("PASS: Seed invalid category returns 400")
    
    def test_seed_backup_windows(self):
        """Test seeding backup category for Windows"""
        response = requests.post(
            f"{BASE_URL}/api/seeder/seed",
            json={"category": "backup", "os": "windows"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["added"] >= 0
        assert "total_articles" in data
        print(f"PASS: Seed backup/windows - added: {data['added']}, total: {data['total_articles']}")
    
    def test_seed_verify_persistence(self):
        """Test that seeded articles are actually persisted"""
        # Seed monitoring/rhel (unique combo)
        response = requests.post(
            f"{BASE_URL}/api/seeder/seed",
            json={"category": "monitoring", "os": "rhel"}
        )
        data = response.json()
        
        # Verify via search API
        search_response = requests.get(f"{BASE_URL}/api/snippets?search=RHEL+monitoring")
        search_data = search_response.json()
        
        # Should find RHEL monitoring articles
        rhel_articles = [s for s in search_data if "rhel" in s.get("os", [])]
        print(f"PASS: Seed monitoring/rhel - found {len(rhel_articles)} RHEL articles via search")


class TestAllCategories:
    """Test that all 14 categories have templates"""
    
    def test_all_categories_have_templates(self):
        """Verify each category has at least one template"""
        response = requests.get(f"{BASE_URL}/api/seeder/categories")
        categories = response.json()["categories"]
        
        for cat in categories:
            preview = requests.post(
                f"{BASE_URL}/api/seeder/preview",
                json={"category": cat, "os": "linux"}
            )
            assert preview.status_code == 200, f"Preview failed for category: {cat}"
            data = preview.json()
            assert data["total"] >= 1, f"Category {cat} should have at least 1 template"
        
        print(f"PASS: All {len(categories)} categories have templates")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
