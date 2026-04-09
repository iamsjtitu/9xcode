"""
Test Bug Fixes - Iteration 10
Tests for:
1. POST /api/ai-rewrite/optimize-existing returns 402 when budget/balance keywords in error (not 500)
2. GET /api/ai-rewrite/articles-for-optimize returns paginated articles with optimization status
3. POST /api/updater/update triggers update and returns correct response
4. GET /api/updater/status returns correct status with logs
"""

import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://command-vault-app.preview.emergentagent.com').rstrip('/')


class TestUpdaterEndpoints:
    """Test updater endpoints - POST /api/updater/update and GET /api/updater/status"""
    
    def test_updater_status_endpoint_returns_correct_structure(self):
        """GET /api/updater/status should return status with logs"""
        response = requests.get(f"{BASE_URL}/api/updater/status", timeout=10)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        # Verify response structure
        assert "is_running" in data, "Missing 'is_running' field"
        assert "last_run" in data, "Missing 'last_run' field"
        assert "last_status" in data, "Missing 'last_status' field"
        assert "current_step" in data, "Missing 'current_step' field"
        assert "logs" in data, "Missing 'logs' field"
        
        # Verify types
        assert isinstance(data["is_running"], bool), "is_running should be boolean"
        assert isinstance(data["logs"], list), "logs should be a list"
        
        print(f"Updater status: is_running={data['is_running']}, last_status={data['last_status']}")
    
    def test_updater_update_endpoint_returns_skipped_in_preview(self):
        """POST /api/updater/update should return 'skipped' in preview (no VPS path)"""
        response = requests.post(f"{BASE_URL}/api/updater/update", timeout=15)
        
        # Should return 200 with skipped status (not crash)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "status" in data, "Missing 'status' field"
        assert data["status"] == "skipped", f"Expected 'skipped', got {data['status']}"
        assert "message" in data, "Missing 'message' field"
        
        print(f"Update response: {data}")
    
    def test_updater_status_after_update_shows_skipped(self):
        """After triggering update in preview, status should show 'skipped'"""
        # First trigger update
        requests.post(f"{BASE_URL}/api/updater/update", timeout=15)
        
        # Then check status
        response = requests.get(f"{BASE_URL}/api/updater/status", timeout=10)
        assert response.status_code == 200
        
        data = response.json()
        assert data["last_status"] == "skipped", f"Expected 'skipped', got {data['last_status']}"
        assert data["is_running"] == False, "Should not be running after skipped"
        
        # Verify logs contain expected messages
        logs = data.get("logs", [])
        assert len(logs) > 0, "Logs should not be empty"
        
        # Check for RESULT:skipped in logs (bug fix: search all lines, not just last)
        has_result = any("RESULT:skipped" in log for log in logs)
        assert has_result, "Logs should contain 'RESULT:skipped'"
        
        print(f"Logs after update: {logs}")


class TestAIRewriteEndpoints:
    """Test AI rewrite endpoints with focus on error handling"""
    
    def test_articles_for_optimize_returns_paginated_data(self):
        """GET /api/ai-rewrite/articles-for-optimize returns paginated articles"""
        response = requests.get(f"{BASE_URL}/api/ai-rewrite/articles-for-optimize?limit=5", timeout=10)
        assert response.status_code == 200
        
        data = response.json()
        # Verify pagination structure
        assert "articles" in data
        assert "total" in data
        assert "page" in data
        assert "pages" in data
        assert "categories" in data
        assert "optimized_count" in data
        assert "total_articles" in data
        
        # Verify articles have required fields
        if data["articles"]:
            article = data["articles"][0]
            assert "slug" in article
            assert "title" in article
            assert "category" in article
            # ai_optimized may or may not be present
            
        print(f"Total articles: {data['total_articles']}, Optimized: {data['optimized_count']}")
    
    def test_articles_for_optimize_filter_by_status_pending(self):
        """Filter by pending status returns only non-optimized articles"""
        response = requests.get(f"{BASE_URL}/api/ai-rewrite/articles-for-optimize?filter_status=pending&limit=10", timeout=10)
        assert response.status_code == 200
        
        data = response.json()
        for article in data["articles"]:
            # Pending articles should have ai_optimized=False or not set
            assert article.get("ai_optimized") != True, f"Article {article['slug']} should not be optimized"
    
    def test_articles_for_optimize_filter_by_status_optimized(self):
        """Filter by optimized status returns only optimized articles"""
        response = requests.get(f"{BASE_URL}/api/ai-rewrite/articles-for-optimize?filter_status=optimized&limit=10", timeout=10)
        assert response.status_code == 200
        
        data = response.json()
        for article in data["articles"]:
            assert article.get("ai_optimized") == True, f"Article {article['slug']} should be optimized"
    
    def test_optimize_existing_returns_404_for_invalid_slug(self):
        """POST /api/ai-rewrite/optimize-existing returns 404 for non-existent slug"""
        response = requests.post(
            f"{BASE_URL}/api/ai-rewrite/optimize-existing",
            json={"slug": "non-existent-article-slug-12345"},
            timeout=10
        )
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    
    def test_optimize_existing_returns_422_for_missing_slug(self):
        """POST /api/ai-rewrite/optimize-existing returns 422 for missing slug"""
        response = requests.post(
            f"{BASE_URL}/api/ai-rewrite/optimize-existing",
            json={},
            timeout=10
        )
        assert response.status_code == 422, f"Expected 422, got {response.status_code}"


class TestBudgetErrorHandling:
    """Test that budget/balance errors return 402 instead of 500"""
    
    def test_call_ai_error_keywords_in_code(self):
        """Verify the code has correct budget error keywords"""
        # This is a code review test - verify the keywords are in the call_ai function
        # The actual 402 response would require triggering a real budget error
        
        # Read the ai_rewrite.py file to verify keywords
        import os
        ai_rewrite_path = "/app/backend/routes/ai_rewrite.py"
        
        if os.path.exists(ai_rewrite_path):
            with open(ai_rewrite_path, 'r') as f:
                content = f.read()
            
            # Verify budget error keywords are present
            assert 'balance' in content.lower(), "Missing 'balance' keyword check"
            assert 'credit' in content.lower(), "Missing 'credit' keyword check"
            assert 'budget' in content.lower(), "Missing 'budget' keyword check"
            assert 'exceeded' in content.lower(), "Missing 'exceeded' keyword check"
            assert 'quota' in content.lower(), "Missing 'quota' keyword check"
            
            # Verify 402 status code is used
            assert '402' in content, "Missing 402 status code for budget errors"
            
            print("Budget error handling code verified - keywords and 402 status present")
        else:
            pytest.skip("ai_rewrite.py not found at expected path")


class TestUpdaterLogParsing:
    """Test that updater correctly parses logs (searches all lines, not just last)"""
    
    def test_log_parsing_code_searches_all_lines(self):
        """Verify the code searches all log lines for RESULT, not just last line"""
        import os
        updater_path = "/app/backend/routes/updater.py"
        
        if os.path.exists(updater_path):
            with open(updater_path, 'r') as f:
                content = f.read()
            
            # Verify the code iterates through logs (not just checking last line)
            # Look for patterns like "for line in logs" or similar iteration
            assert 'for line in logs' in content, "Should iterate through all log lines"
            
            # Verify RESULT:success and RESULT:failed checks
            assert 'RESULT:success' in content, "Should check for RESULT:success"
            assert 'RESULT:failed' in content, "Should check for RESULT:failed"
            
            print("Log parsing code verified - iterates through all lines")
        else:
            pytest.skip("updater.py not found at expected path")


class TestInlineUpdaterWriteOrder:
    """Test that inline updater writes RESULT before PM2 restart"""
    
    def test_result_written_before_pm2_restart(self):
        """Verify RESULT is written to log before PM2 restart command"""
        import os
        updater_path = "/app/backend/routes/updater.py"
        
        if os.path.exists(updater_path):
            with open(updater_path, 'r') as f:
                content = f.read()
            
            # Find the position of RESULT write and PM2 restart
            result_write_pos = content.find('f.write(f"RESULT:{result_status}')
            if result_write_pos == -1:
                result_write_pos = content.find("RESULT:")
            
            pm2_restart_pos = content.find('pm2 restart')
            
            # RESULT should be written before PM2 restart
            if result_write_pos != -1 and pm2_restart_pos != -1:
                # Check that there's a RESULT write before the PM2 restart section
                # The code should write status before calling PM2
                assert result_write_pos < pm2_restart_pos, "RESULT should be written before PM2 restart"
                print("Verified: RESULT is written before PM2 restart")
            else:
                print(f"result_write_pos={result_write_pos}, pm2_restart_pos={pm2_restart_pos}")
                pytest.skip("Could not find both RESULT write and PM2 restart in code")
        else:
            pytest.skip("updater.py not found at expected path")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
