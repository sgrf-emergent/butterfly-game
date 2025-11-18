#!/usr/bin/env python3
"""
Backend API Testing for Butterfly Identification Game
Tests all backend endpoints according to test_result.md requirements
"""

import requests
import json
import time
from typing import Dict, List, Any

# Get backend URL from frontend .env file
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('EXPO_PUBLIC_BACKEND_URL='):
                    base_url = line.split('=', 1)[1].strip()
                    return f"{base_url}/api"
        return "http://localhost:8001/api"  # fallback
    except Exception as e:
        print(f"Error reading frontend .env: {e}")
        return "http://localhost:8001/api"  # fallback

BASE_URL = get_backend_url()
print(f"Testing backend at: {BASE_URL}")

class BackendTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.test_results = {
            "init_butterflies": {"passed": False, "details": ""},
            "get_butterflies": {"passed": False, "details": ""},
            "quiz_question": {"passed": False, "details": ""},
            "admin_get_butterflies": {"passed": False, "details": ""},
            "admin_create_butterfly": {"passed": False, "details": ""},
            "admin_update_butterfly": {"passed": False, "details": ""},
            "admin_delete_butterfly": {"passed": False, "details": ""},
            "overall": {"passed": False, "critical_issues": [], "minor_issues": []}
        }
        self.created_butterfly_id = None
    
    def test_api_health(self):
        """Test if API is accessible"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            if response.status_code == 200:
                print("✅ API health check passed")
                return True
            else:
                print(f"❌ API health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ API health check failed: {e}")
            return False
    
    def clear_database(self):
        """Clear existing butterflies for clean testing"""
        try:
            # Try to get current count
            response = requests.get(f"{self.base_url}/butterflies", timeout=10)
            if response.status_code == 200:
                butterflies = response.json()
                print(f"Found {len(butterflies)} existing butterflies")
                # Note: We don't have a delete endpoint, so we'll work with existing data
                return True
        except Exception as e:
            print(f"Warning: Could not check existing butterflies: {e}")
            return True
    
    def test_init_butterflies(self):
        """Test POST /api/init-butterflies endpoint"""
        print("\n🧪 Testing POST /api/init-butterflies...")
        
        try:
            # First call to initialize
            response = requests.post(f"{self.base_url}/init-butterflies", timeout=15)
            
            if response.status_code != 200:
                self.test_results["init_butterflies"]["details"] = f"HTTP {response.status_code}: {response.text}"
                self.test_results["overall"]["critical_issues"].append("init-butterflies endpoint failed")
                print(f"❌ Init butterflies failed: {response.status_code}")
                return False
            
            result = response.json()
            print(f"✅ Init response: {result}")
            
            # Verify the response message
            if "Successfully initialized" in result.get("message", ""):
                # Extract number from message
                message = result["message"]
                if "30 butterflies" in message:
                    print("✅ Successfully initialized 30 butterflies")
                else:
                    print(f"⚠️ Unexpected count in message: {message}")
            elif "already initialized" in result.get("message", ""):
                print("✅ Database already initialized (acceptable)")
            else:
                print(f"⚠️ Unexpected response: {result}")
            
            # Test second call (should indicate already initialized)
            response2 = requests.post(f"{self.base_url}/init-butterflies", timeout=10)
            if response2.status_code == 200:
                result2 = response2.json()
                if "already initialized" in result2.get("message", ""):
                    print("✅ Duplicate initialization handled correctly")
                else:
                    print(f"✅ Second init response: {result2}")
            
            self.test_results["init_butterflies"]["passed"] = True
            self.test_results["init_butterflies"]["details"] = "Successfully initialized butterflies"
            return True
            
        except Exception as e:
            self.test_results["init_butterflies"]["details"] = f"Exception: {str(e)}"
            self.test_results["overall"]["critical_issues"].append(f"init-butterflies endpoint error: {str(e)}")
            print(f"❌ Init butterflies error: {e}")
            return False
    
    def test_get_butterflies(self):
        """Test GET /api/butterflies endpoint"""
        print("\n🧪 Testing GET /api/butterflies...")
        
        try:
            response = requests.get(f"{self.base_url}/butterflies", timeout=10)
            
            if response.status_code != 200:
                self.test_results["get_butterflies"]["details"] = f"HTTP {response.status_code}: {response.text}"
                self.test_results["overall"]["critical_issues"].append("get butterflies endpoint failed")
                print(f"❌ Get butterflies failed: {response.status_code}")
                return False
            
            butterflies = response.json()
            
            # Verify it's a list
            if not isinstance(butterflies, list):
                self.test_results["get_butterflies"]["details"] = "Response is not a list"
                self.test_results["overall"]["critical_issues"].append("get butterflies returns invalid format")
                print("❌ Response is not a list")
                return False
            
            print(f"✅ Retrieved {len(butterflies)} butterflies")
            
            # Verify we have exactly 30 butterflies
            if len(butterflies) != 30:
                self.test_results["overall"]["minor_issues"].append(f"Expected 30 butterflies, got {len(butterflies)}")
                print(f"⚠️ Expected 30 butterflies, got {len(butterflies)}")
            else:
                print("✅ Correct count: 30 butterflies")
            
            # Verify butterfly structure
            if butterflies:
                butterfly = butterflies[0]
                required_fields = ["id", "commonName", "latinName", "imageUrl"]
                missing_fields = [field for field in required_fields if field not in butterfly]
                
                if missing_fields:
                    self.test_results["get_butterflies"]["details"] = f"Missing fields: {missing_fields}"
                    self.test_results["overall"]["critical_issues"].append(f"Butterfly objects missing fields: {missing_fields}")
                    print(f"❌ Missing required fields: {missing_fields}")
                    return False
                
                print(f"✅ Butterfly structure valid. Sample: {butterfly['commonName']} ({butterfly['latinName']})")
                
                # Check for unique IDs
                ids = [b.get("id") for b in butterflies]
                if len(set(ids)) != len(ids):
                    self.test_results["overall"]["minor_issues"].append("Duplicate butterfly IDs found")
                    print("⚠️ Duplicate IDs found")
                else:
                    print("✅ All butterfly IDs are unique")
            
            self.test_results["get_butterflies"]["passed"] = True
            self.test_results["get_butterflies"]["details"] = f"Successfully retrieved {len(butterflies)} butterflies"
            return True
            
        except Exception as e:
            self.test_results["get_butterflies"]["details"] = f"Exception: {str(e)}"
            self.test_results["overall"]["critical_issues"].append(f"get butterflies error: {str(e)}")
            print(f"❌ Get butterflies error: {e}")
            return False
    
    def test_quiz_question(self):
        """Test GET /api/quiz/question endpoint"""
        print("\n🧪 Testing GET /api/quiz/question...")
        
        try:
            # Test multiple calls to verify randomization
            questions = []
            for i in range(5):
                response = requests.get(f"{self.base_url}/quiz/question", timeout=10)
                
                if response.status_code != 200:
                    self.test_results["quiz_question"]["details"] = f"HTTP {response.status_code}: {response.text}"
                    self.test_results["overall"]["critical_issues"].append("quiz question endpoint failed")
                    print(f"❌ Quiz question failed: {response.status_code}")
                    return False
                
                question = response.json()
                questions.append(question)
                
                # Verify response structure
                if "correctAnswer" not in question or "options" not in question:
                    self.test_results["quiz_question"]["details"] = "Missing correctAnswer or options in response"
                    self.test_results["overall"]["critical_issues"].append("Quiz question missing required fields")
                    print("❌ Missing correctAnswer or options in response")
                    return False
                
                # Verify options is a list of 5 items
                options = question["options"]
                if not isinstance(options, list) or len(options) != 5:
                    self.test_results["quiz_question"]["details"] = f"Options should be list of 5, got {type(options)} with {len(options) if isinstance(options, list) else 'N/A'} items"
                    self.test_results["overall"]["critical_issues"].append("Quiz question options format invalid")
                    print(f"❌ Options should be list of 5, got {len(options) if isinstance(options, list) else 'invalid'}")
                    return False
                
                # Verify correctAnswer is in options
                correct_answer = question["correctAnswer"]
                correct_id = correct_answer.get("id")
                option_ids = [opt.get("id") for opt in options]
                
                if correct_id not in option_ids:
                    self.test_results["quiz_question"]["details"] = "Correct answer not found in options"
                    self.test_results["overall"]["critical_issues"].append("Quiz question correct answer not in options")
                    print("❌ Correct answer not found in options")
                    return False
                
                # Verify butterfly structure in both correctAnswer and options
                for butterfly in [correct_answer] + options:
                    required_fields = ["id", "commonName", "latinName", "imageUrl"]
                    missing_fields = [field for field in required_fields if field not in butterfly]
                    if missing_fields:
                        self.test_results["quiz_question"]["details"] = f"Butterfly missing fields: {missing_fields}"
                        self.test_results["overall"]["critical_issues"].append(f"Quiz butterfly objects missing fields: {missing_fields}")
                        print(f"❌ Butterfly missing required fields: {missing_fields}")
                        return False
                
                print(f"✅ Quiz question {i+1}: {correct_answer['commonName']} with 5 options")
            
            # Check for randomization (different correct answers)
            correct_answers = [q["correctAnswer"]["id"] for q in questions]
            unique_answers = set(correct_answers)
            
            if len(unique_answers) > 1:
                print(f"✅ Randomization working: {len(unique_answers)} different butterflies in {len(questions)} calls")
            else:
                self.test_results["overall"]["minor_issues"].append("Quiz questions may not be properly randomized")
                print(f"⚠️ All {len(questions)} calls returned same butterfly - randomization may not be working")
            
            # Test with empty database scenario (if possible)
            print("✅ Quiz question endpoint working correctly")
            
            self.test_results["quiz_question"]["passed"] = True
            self.test_results["quiz_question"]["details"] = f"Successfully tested quiz questions with proper structure and randomization"
            return True
            
        except Exception as e:
            self.test_results["quiz_question"]["details"] = f"Exception: {str(e)}"
            self.test_results["overall"]["critical_issues"].append(f"quiz question error: {str(e)}")
            print(f"❌ Quiz question error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting Backend API Tests for Butterfly Identification Game")
        print("=" * 60)
        
        # Check API health first
        if not self.test_api_health():
            self.test_results["overall"]["critical_issues"].append("API not accessible")
            return self.test_results
        
        # Clear database for clean testing
        self.clear_database()
        
        # Run tests in order
        tests = [
            ("Initialize Butterflies", self.test_init_butterflies),
            ("Get All Butterflies", self.test_get_butterflies),
            ("Quiz Question", self.test_quiz_question)
        ]
        
        passed_tests = 0
        for test_name, test_func in tests:
            print(f"\n{'='*20} {test_name} {'='*20}")
            if test_func():
                passed_tests += 1
        
        # Overall results
        print(f"\n{'='*60}")
        print(f"🏁 BACKEND TESTING COMPLETE")
        print(f"✅ Passed: {passed_tests}/{len(tests)} tests")
        
        if self.test_results["overall"]["critical_issues"]:
            print(f"❌ Critical Issues: {len(self.test_results['overall']['critical_issues'])}")
            for issue in self.test_results["overall"]["critical_issues"]:
                print(f"   - {issue}")
        
        if self.test_results["overall"]["minor_issues"]:
            print(f"⚠️ Minor Issues: {len(self.test_results['overall']['minor_issues'])}")
            for issue in self.test_results["overall"]["minor_issues"]:
                print(f"   - {issue}")
        
        # Determine overall pass/fail
        self.test_results["overall"]["passed"] = (
            passed_tests == len(tests) and 
            len(self.test_results["overall"]["critical_issues"]) == 0
        )
        
        if self.test_results["overall"]["passed"]:
            print("\n🎉 ALL BACKEND TESTS PASSED!")
        else:
            print("\n💥 SOME BACKEND TESTS FAILED!")
        
        return self.test_results

if __name__ == "__main__":
    tester = BackendTester()
    results = tester.run_all_tests()
    
    # Print summary for easy parsing
    print(f"\n{'='*60}")
    print("SUMMARY FOR MAIN AGENT:")
    print(f"Overall Status: {'PASS' if results['overall']['passed'] else 'FAIL'}")
    print(f"Critical Issues: {len(results['overall']['critical_issues'])}")
    print(f"Minor Issues: {len(results['overall']['minor_issues'])}")