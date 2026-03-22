#!/usr/bin/env python3
"""
9xCodes Backend API Testing Suite
Tests all backend API endpoints for the 9xCodes application
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, Any, List

# Base URL from frontend environment
BASE_URL = "https://auto-content-18.preview.emergentagent.com/api"

class BackendTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.test_results = []
        self.created_snippet_slug = None
        self.created_snippet_id = None
        
    def log_test(self, test_name: str, success: bool, message: str, details: Dict = None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "details": details or {}
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if details and not success:
            print(f"   Details: {details}")
    
    def test_get_all_snippets(self):
        """Test GET /api/snippets - Fetch all code snippets"""
        try:
            response = self.session.get(f"{self.base_url}/snippets")
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify response is an array
                if not isinstance(data, list):
                    self.log_test("GET /api/snippets", False, "Response is not an array", 
                                {"response_type": type(data).__name__})
                    return
                
                # Check if snippets have required fields
                if len(data) > 0:
                    snippet = data[0]
                    required_fields = ['id', 'title', 'slug', 'description', 'category', 'os', 'difficulty', 'tags', 'steps']
                    missing_fields = [field for field in required_fields if field not in snippet]
                    
                    if missing_fields:
                        self.log_test("GET /api/snippets", False, f"Missing required fields: {missing_fields}",
                                    {"snippet_sample": snippet})
                        return
                    
                    # Store first snippet for later tests
                    if self.created_snippet_slug is None:
                        self.created_snippet_slug = snippet.get('slug')
                        self.created_snippet_id = snippet.get('id')
                
                self.log_test("GET /api/snippets", True, f"Retrieved {len(data)} snippets successfully",
                            {"count": len(data)})
            else:
                self.log_test("GET /api/snippets", False, f"HTTP {response.status_code}: {response.text}",
                            {"status_code": response.status_code})
                
        except Exception as e:
            self.log_test("GET /api/snippets", False, f"Request failed: {str(e)}")
    
    def test_get_snippet_by_slug(self):
        """Test GET /api/snippets/{slug} - Fetch single snippet by slug"""
        # First try with the test slug from requirements
        test_slug = "install-cpanel-ubuntu"
        
        try:
            # Get initial views count
            response = self.session.get(f"{self.base_url}/snippets/{test_slug}")
            
            if response.status_code == 404:
                # If test slug doesn't exist, use any available slug
                if self.created_snippet_slug:
                    test_slug = self.created_snippet_slug
                    response = self.session.get(f"{self.base_url}/snippets/{test_slug}")
                else:
                    self.log_test("GET /api/snippets/{slug}", False, "No snippets available for testing")
                    return
            
            if response.status_code == 200:
                snippet1 = response.json()
                initial_views = snippet1.get('views', 0)
                
                # Make another request to verify views increment
                response2 = self.session.get(f"{self.base_url}/snippets/{test_slug}")
                
                if response2.status_code == 200:
                    snippet2 = response2.json()
                    new_views = snippet2.get('views', 0)
                    
                    # Check if views incremented
                    if new_views > initial_views:
                        # Verify all required fields are present
                        required_fields = ['id', 'title', 'slug', 'description', 'category', 'os', 'difficulty', 'tags', 'steps']
                        missing_fields = [field for field in required_fields if field not in snippet2]
                        
                        if missing_fields:
                            self.log_test("GET /api/snippets/{slug}", False, f"Missing fields: {missing_fields}",
                                        {"snippet": snippet2})
                        else:
                            self.log_test("GET /api/snippets/{slug}", True, 
                                        f"Retrieved snippet '{test_slug}' and views incremented from {initial_views} to {new_views}",
                                        {"slug": test_slug, "views_increment": True})
                    else:
                        self.log_test("GET /api/snippets/{slug}", False, 
                                    f"Views did not increment (stayed at {initial_views})",
                                    {"slug": test_slug, "views_increment": False})
                else:
                    self.log_test("GET /api/snippets/{slug}", False, f"Second request failed: HTTP {response2.status_code}")
            else:
                self.log_test("GET /api/snippets/{slug}", False, f"HTTP {response.status_code}: {response.text}",
                            {"status_code": response.status_code, "slug": test_slug})
                
        except Exception as e:
            self.log_test("GET /api/snippets/{slug}", False, f"Request failed: {str(e)}")
    
    def test_create_snippet(self):
        """Test POST /api/snippets - Create new code snippet"""
        test_snippet = {
            "title": "Test Docker Installation Guide",
            "description": "A comprehensive guide to install Docker on various systems",
            "category": "DevOps",
            "os": ["Ubuntu", "CentOS"],
            "difficulty": "Intermediate",
            "tags": ["docker", "containerization", "devops"],
            "steps": [
                {
                    "title": "Update System Packages",
                    "description": "Update your system packages to the latest version",
                    "code": "sudo apt update && sudo apt upgrade -y",
                    "language": "bash"
                },
                {
                    "title": "Install Docker",
                    "description": "Install Docker using the official repository",
                    "code": "curl -fsSL https://get.docker.com -o get-docker.sh\nsudo sh get-docker.sh",
                    "language": "bash"
                }
            ],
            "postInstallation": {
                "title": "Verify Installation",
                "content": "Run 'docker --version' to verify the installation was successful."
            }
        }
        
        try:
            response = self.session.post(f"{self.base_url}/snippets", json=test_snippet)
            
            if response.status_code == 200:
                created_snippet = response.json()
                
                # Verify slug was auto-generated
                if 'slug' not in created_snippet:
                    self.log_test("POST /api/snippets", False, "Slug was not auto-generated")
                    return
                
                # Verify response includes created snippet with all fields
                required_fields = ['id', 'title', 'slug', 'description', 'category', 'os', 'difficulty', 'tags', 'steps']
                missing_fields = [field for field in required_fields if field not in created_snippet]
                
                if missing_fields:
                    self.log_test("POST /api/snippets", False, f"Missing fields in response: {missing_fields}",
                                {"created_snippet": created_snippet})
                else:
                    # Store for later tests
                    self.created_snippet_slug = created_snippet['slug']
                    self.created_snippet_id = created_snippet['id']
                    
                    self.log_test("POST /api/snippets", True, 
                                f"Created snippet with slug '{created_snippet['slug']}'",
                                {"slug": created_snippet['slug'], "id": created_snippet['id']})
            else:
                self.log_test("POST /api/snippets", False, f"HTTP {response.status_code}: {response.text}",
                            {"status_code": response.status_code})
                
        except Exception as e:
            self.log_test("POST /api/snippets", False, f"Request failed: {str(e)}")
    
    def test_like_snippet(self):
        """Test POST /api/snippets/{slug}/like - Like a snippet"""
        # Try with the specified slug first
        test_slug = "ssh-security-hardening"
        
        try:
            response = self.session.post(f"{self.base_url}/snippets/{test_slug}/like")
            
            if response.status_code == 404:
                # If specified slug doesn't exist, use any available slug
                if self.created_snippet_slug:
                    test_slug = self.created_snippet_slug
                    response = self.session.post(f"{self.base_url}/snippets/{test_slug}/like")
                else:
                    self.log_test("POST /api/snippets/{slug}/like", False, "No snippets available for testing")
                    return
            
            if response.status_code == 200:
                like_response = response.json()
                
                if 'likes' in like_response:
                    likes_count = like_response['likes']
                    self.log_test("POST /api/snippets/{slug}/like", True, 
                                f"Successfully liked snippet '{test_slug}', likes count: {likes_count}",
                                {"slug": test_slug, "likes": likes_count})
                else:
                    self.log_test("POST /api/snippets/{slug}/like", False, 
                                "Response missing 'likes' field",
                                {"response": like_response})
            else:
                self.log_test("POST /api/snippets/{slug}/like", False, f"HTTP {response.status_code}: {response.text}",
                            {"status_code": response.status_code, "slug": test_slug})
                
        except Exception as e:
            self.log_test("POST /api/snippets/{slug}/like", False, f"Request failed: {str(e)}")
    
    def test_get_ads_config(self):
        """Test GET /api/ads/config - Get Google Ads configuration"""
        try:
            response = self.session.get(f"{self.base_url}/ads/config")
            
            if response.status_code == 200:
                config = response.json()
                
                # Check required structure
                required_fields = ['enabled', 'headerAdCode', 'sidebarAdCode', 'betweenSnippetsAdCode', 'footerAdCode']
                missing_fields = [field for field in required_fields if field not in config]
                
                if missing_fields:
                    self.log_test("GET /api/ads/config", False, f"Missing fields: {missing_fields}",
                                {"config": config})
                else:
                    self.log_test("GET /api/ads/config", True, 
                                f"Retrieved ads config successfully, enabled: {config.get('enabled')}",
                                {"config_structure": list(config.keys())})
            else:
                self.log_test("GET /api/ads/config", False, f"HTTP {response.status_code}: {response.text}",
                            {"status_code": response.status_code})
                
        except Exception as e:
            self.log_test("GET /api/ads/config", False, f"Request failed: {str(e)}")
    
    def test_update_ads_config(self):
        """Test PUT /api/ads/config - Update Google Ads configuration"""
        test_config = {
            "enabled": True,
            "headerAdCode": "<script>console.log('Header Ad');</script>",
            "sidebarAdCode": "<div>Sidebar Ad Content</div>",
            "betweenSnippetsAdCode": "<div>Between Snippets Ad</div>",
            "footerAdCode": "<footer>Footer Ad Content</footer>"
        }
        
        try:
            response = self.session.put(f"{self.base_url}/ads/config", json=test_config)
            
            if response.status_code == 200:
                updated_config = response.json()
                
                # Verify updated config is returned with correct values
                config_matches = all(
                    updated_config.get(key) == value 
                    for key, value in test_config.items()
                )
                
                if config_matches:
                    self.log_test("PUT /api/ads/config", True, 
                                "Successfully updated ads configuration",
                                {"enabled": updated_config.get('enabled')})
                else:
                    self.log_test("PUT /api/ads/config", False, 
                                "Updated config doesn't match sent values",
                                {"sent": test_config, "received": updated_config})
            else:
                self.log_test("PUT /api/ads/config", False, f"HTTP {response.status_code}: {response.text}",
                            {"status_code": response.status_code})
                
        except Exception as e:
            self.log_test("PUT /api/ads/config", False, f"Request failed: {str(e)}")
    
    def test_create_comment(self):
        """Test POST /api/comments - Create comment"""
        if not self.created_snippet_id:
            self.log_test("POST /api/comments", False, "No snippet ID available for testing")
            return
        
        test_comment = {
            "snippetId": self.created_snippet_id,
            "user": "TestUser",
            "text": "This is a test comment for the code snippet. Very helpful guide!"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/comments", json=test_comment)
            
            if response.status_code == 200:
                created_comment = response.json()
                
                # Verify comment is created with proper fields
                required_fields = ['id', 'snippetId', 'user', 'text', 'createdAt']
                missing_fields = [field for field in required_fields if field not in created_comment]
                
                if missing_fields:
                    self.log_test("POST /api/comments", False, f"Missing fields: {missing_fields}",
                                {"comment": created_comment})
                else:
                    self.log_test("POST /api/comments", True, 
                                f"Created comment successfully for snippet {self.created_snippet_id}",
                                {"comment_id": created_comment.get('id')})
            else:
                self.log_test("POST /api/comments", False, f"HTTP {response.status_code}: {response.text}",
                            {"status_code": response.status_code})
                
        except Exception as e:
            self.log_test("POST /api/comments", False, f"Request failed: {str(e)}")
    
    def test_get_comments(self):
        """Test GET /api/comments/{snippet_id} - Get comments for a snippet"""
        if not self.created_snippet_id:
            self.log_test("GET /api/comments/{snippet_id}", False, "No snippet ID available for testing")
            return
        
        try:
            response = self.session.get(f"{self.base_url}/comments/{self.created_snippet_id}")
            
            if response.status_code == 200:
                comments = response.json()
                
                # Verify array is returned
                if not isinstance(comments, list):
                    self.log_test("GET /api/comments/{snippet_id}", False, "Response is not an array",
                                {"response_type": type(comments).__name__})
                else:
                    self.log_test("GET /api/comments/{snippet_id}", True, 
                                f"Retrieved {len(comments)} comments for snippet {self.created_snippet_id}",
                                {"comment_count": len(comments)})
            else:
                self.log_test("GET /api/comments/{snippet_id}", False, f"HTTP {response.status_code}: {response.text}",
                            {"status_code": response.status_code})
                
        except Exception as e:
            self.log_test("GET /api/comments/{snippet_id}", False, f"Request failed: {str(e)}")
    
    def run_all_tests(self):
        """Run all backend API tests"""
        print(f"🚀 Starting 9xCodes Backend API Tests")
        print(f"📍 Base URL: {self.base_url}")
        print("=" * 60)
        
        # Run tests in logical order
        self.test_get_all_snippets()
        self.test_get_snippet_by_slug()
        self.test_create_snippet()
        self.test_like_snippet()
        self.test_get_ads_config()
        self.test_update_ads_config()
        self.test_create_comment()
        self.test_get_comments()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result['success'])
        failed = len(self.test_results) - passed
        
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📈 Success Rate: {(passed/len(self.test_results)*100):.1f}%")
        
        if failed > 0:
            print("\n🔍 FAILED TESTS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   • {result['test']}: {result['message']}")
        
        return passed, failed

if __name__ == "__main__":
    tester = BackendTester()
    passed, failed = tester.run_all_tests()
    
    # Exit with error code if any tests failed
    sys.exit(0 if failed == 0 else 1)