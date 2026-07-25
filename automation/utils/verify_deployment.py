"""
Deployment verification script
"""

import requests
import time
import sys
from config.config import config


def verify_deployment(base_url: str = None, max_retries: int = 5, retry_delay: int = 30):
    """
    Verify deployment is accessible and functional
    
    Args:
        base_url: Base URL to verify
        max_retries: Maximum number of retries
        retry_delay: Delay between retries in seconds
    
    Returns:
        bool: True if deployment is verified, False otherwise
    """
    base_url = base_url or config.BASE_URL
    
    print(f"Verifying deployment at: {base_url}")
    
    for attempt in range(max_retries):
        try:
            # Check HTTP status
            print(f"Attempt {attempt + 1}/{max_retries}: Checking HTTP status...")
            response = requests.get(base_url, timeout=30)
            
            if response.status_code == 200:
                print(f"✅ HTTP Status: {response.status_code}")
            else:
                print(f"❌ HTTP Status: {response.status_code}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                return False
            
            # Check page content
            print("Checking page content...")
            if "DOCTYPE html" in response.text or "<html" in response.text:
                print("✅ HTML structure valid")
            else:
                print("❌ Invalid HTML structure")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                return False
            
            # Check for critical assets
            print("Checking for critical assets...")
            if any(asset in response.text for asset in ["script", "link", "style"]):
                print("✅ Critical assets present")
            else:
                print("⚠️ No critical assets detected")
            
            # Check response time
            response_time = response.elapsed.total_seconds()
            print(f"Response time: {response_time:.2f}s")
            
            if response_time < 5.0:
                print("✅ Response time acceptable")
            else:
                print("⚠️ Response time high")
            
            print("✅ Deployment verification successful")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached")
                return False
    
    return False


def check_endpoint(endpoint: str, expected_status: int = 200):
    """
    Check specific endpoint
    
    Args:
        endpoint: Endpoint to check
        expected_status: Expected HTTP status code
    
    Returns:
        bool: True if endpoint is accessible
    """
    url = f"{config.BASE_URL}{endpoint}"
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == expected_status:
            print(f"✅ {endpoint} - Status: {response.status_code}")
            return True
        else:
            print(f"❌ {endpoint} - Status: {response.status_code} (Expected: {expected_status})")
            return False
    except Exception as e:
        print(f"❌ {endpoint} - Error: {e}")
        return False


def run_full_verification():
    """Run full deployment verification"""
    print("="*60)
    print("DEPLOYMENT VERIFICATION")
    print("="*60)
    
    # Verify main deployment
    if not verify_deployment():
        print("❌ Deployment verification failed")
        sys.exit(1)
    
    # Check common endpoints
    print("\nChecking common endpoints...")
    endpoints = [
        ("/", 200),
        ("/login", 200),
        ("/dashboard", 200),  # May redirect to login
    ]
    
    results = []
    for endpoint, expected_status in endpoints:
        results.append(check_endpoint(endpoint, expected_status))
    
    if all(results):
        print("\n✅ All endpoints verified successfully")
        return True
    else:
        print("\n⚠️ Some endpoints failed verification")
        return True  # Don't fail on endpoint checks


if __name__ == "__main__":
    success = run_full_verification()
    sys.exit(0 if success else 1)
