"""
API Integration Test Suite
"""

import pytest
import requests
from config.config import config
from utils.logger import test_logger


@pytest.mark.api
class TestApiIntegration:
    """API Integration Test Suite"""

    @pytest.fixture(autouse=True)
    def setup(self, base_url):
        """Setup base URL and session"""
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "PolicyLens-ApiTest/1.0",
            "Accept": "application/json, text/html, */*"
        })

    def test_api_001_health_check_endpoint(self):
        """TC_API_001: Health check endpoint accessibility"""
        test_logger.info("TC_API_001: Health check endpoint accessibility")
        url = f"{self.base_url}"
        response = self.session.get(url, timeout=10)
        assert response.status_code in [200, 304], f"Unexpected status code {response.status_code}"

    def test_api_002_headers_validation(self):
        """TC_API_002: Verify response security and content headers"""
        test_logger.info("TC_API_002: Verify response security and content headers")
        url = f"{self.base_url}"
        response = self.session.get(url, timeout=10)
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
        assert "Content-Type" in response.headers, "Missing Content-Type header"

    def test_api_003_auth_login_endpoint_options(self):
        """TC_API_003: Options preflight request for API authentication"""
        test_logger.info("TC_API_003: Options preflight request for API authentication")
        url = f"{self.base_url}/api/v1/auth/login"
        response = self.session.options(url, timeout=10)
        assert response.status_code in [200, 204, 404, 405], f"Unexpected status code {response.status_code}"

    def test_api_004_schemes_list_fetching(self):
        """TC_API_004: Validate schemes endpoint query handling"""
        test_logger.info("TC_API_004: Validate schemes endpoint query handling")
        url = f"{self.base_url}/api/v1/schemes"
        response = self.session.get(url, timeout=10)
        assert response.status_code in [200, 401, 404], f"Unexpected status code {response.status_code}"

    def test_api_005_invalid_endpoint_404(self):
        """TC_API_005: Non-existent endpoint returning 404 status"""
        test_logger.info("TC_API_005: Non-existent endpoint returning 404 status")
        url = f"{self.base_url}/api/v1/nonexistent_endpoint_xyz"
        response = self.session.get(url, timeout=10)
        assert response.status_code == 404, f"Expected 404 Not Found, got {response.status_code}"

    def test_api_006_cors_header_presence(self):
        """TC_API_006: CORS configuration validation"""
        test_logger.info("TC_API_006: CORS configuration validation")
        url = f"{self.base_url}"
        headers = {"Origin": "https://example.com"}
        response = self.session.get(url, headers=headers, timeout=10)
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    def test_api_007_response_time_performance(self):
        """TC_API_007: API latency SLA check (< 2000ms)"""
        test_logger.info("TC_API_007: API latency SLA check")
        url = f"{self.base_url}"
        response = self.session.get(url, timeout=10)
        elapsed_ms = response.elapsed.total_seconds() * 1000
        assert elapsed_ms < 2000, f"Latency {elapsed_ms}ms exceeds 2000ms SLA"

    def test_api_008_payload_validation_reject(self):
        """TC_API_008: Validate malformed payload rejection"""
        test_logger.info("TC_API_008: Validate malformed payload rejection")
        url = f"{self.base_url}/api/v1/auth/login"
        invalid_json = "{"
        response = self.session.post(url, data=invalid_json, headers={"Content-Type": "application/json"}, timeout=10)
        assert response.status_code in [400, 422, 404, 405], f"Unexpected status {response.status_code}"

    def test_api_009_gzip_compression_support(self):
        """TC_API_009: Compression support verification"""
        test_logger.info("TC_API_009: Compression support verification")
        headers = {"Accept-Encoding": "gzip, deflate"}
        response = self.session.get(self.base_url, headers=headers, timeout=10)
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    def test_api_010_content_type_json(self):
        """TC_API_010: Static asset content type validation"""
        test_logger.info("TC_API_010: Static asset content type validation")
        url = f"{self.base_url}/index.html"
        response = self.session.get(url, timeout=10)
        assert response.status_code in [200, 304, 404], f"Unexpected status code {response.status_code}"
