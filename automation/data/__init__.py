"""
Test data package
"""

import json
import os
from typing import Dict, Any


class TestDataManager:
    """Test data manager"""
    
    def __init__(self):
        self.data_dir = os.path.dirname(os.path.abspath(__file__))
        self.test_data_file = os.path.join(self.data_dir, "test_data.json")
        self._load_data()
    
    def _load_data(self):
        """Load test data from JSON file"""
        with open(self.test_data_file, 'r') as f:
            self.data = json.load(f)
    
    def get_user(self, user_type: str) -> Dict[str, Any]:
        """Get user data by type"""
        return self.data.get("users", {}).get(user_type, {})
    
    def get_scheme(self, scheme_type: str) -> Dict[str, Any]:
        """Get scheme data by type"""
        return self.data.get("schemes", {}).get(scheme_type, {})
    
    def get_valid_emails(self) -> list:
        """Get list of valid emails"""
        return self.data.get("validation", {}).get("valid_emails", [])
    
    def get_invalid_emails(self) -> list:
        """Get list of invalid emails"""
        return self.data.get("validation", {}).get("invalid_emails", [])
    
    def get_valid_passwords(self) -> list:
        """Get list of valid passwords"""
        return self.data.get("validation", {}).get("valid_passwords", [])
    
    def get_invalid_passwords(self) -> list:
        """Get list of invalid passwords"""
        return self.data.get("validation", {}).get("invalid_passwords", [])
    
    def get_performance_thresholds(self) -> Dict[str, float]:
        """Get performance thresholds"""
        return self.data.get("performance", {}).get("thresholds", {})


# Global test data manager instance
test_data_manager = TestDataManager()
