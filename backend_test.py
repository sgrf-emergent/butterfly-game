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

    def test_admin_get_butterflies(self):
        """Test GET /api/admin/butterflies endpoint"""
        print("\n🧪 Testing GET /api/admin/butterflies...")
        
        try:
            response = requests.get(f"{self.base_url}/admin/butterflies", timeout=10)
            
            if response.status_code != 200:
                self.test_results["admin_get_butterflies"]["details"] = f"HTTP {response.status_code}: {response.text}"
                self.test_results["overall"]["critical_issues"].append("admin get butterflies endpoint failed")
                print(f"❌ Admin get butterflies failed: {response.status_code}")
                return False
            
            butterflies = response.json()
            
            # Verify it's a list
            if not isinstance(butterflies, list):
                self.test_results["admin_get_butterflies"]["details"] = "Response is not a list"
                self.test_results["overall"]["critical_issues"].append("admin get butterflies returns invalid format")
                print("❌ Response is not a list")
                return False
            
            print(f"✅ Admin retrieved {len(butterflies)} butterflies")
            
            # Verify we have butterflies (should be 30 from initialization)
            if len(butterflies) == 0:
                self.test_results["overall"]["critical_issues"].append("No butterflies found in admin endpoint")
                print("❌ No butterflies found")
                return False
            
            # Verify butterfly structure
            if butterflies:
                butterfly = butterflies[0]
                required_fields = ["id", "commonName", "latinName", "imageUrl", "difficulty"]
                missing_fields = [field for field in required_fields if field not in butterfly]
                
                if missing_fields:
                    self.test_results["admin_get_butterflies"]["details"] = f"Missing fields: {missing_fields}"
                    self.test_results["overall"]["critical_issues"].append(f"Admin butterfly objects missing fields: {missing_fields}")
                    print(f"❌ Missing required fields: {missing_fields}")
                    return False
                
                print(f"✅ Admin butterfly structure valid. Sample: {butterfly['commonName']} ({butterfly['latinName']})")
            
            self.test_results["admin_get_butterflies"]["passed"] = True
            self.test_results["admin_get_butterflies"]["details"] = f"Successfully retrieved {len(butterflies)} butterflies via admin endpoint"
            return True
            
        except Exception as e:
            self.test_results["admin_get_butterflies"]["details"] = f"Exception: {str(e)}"
            self.test_results["overall"]["critical_issues"].append(f"admin get butterflies error: {str(e)}")
            print(f"❌ Admin get butterflies error: {e}")
            return False

    def test_admin_create_butterfly(self):
        """Test POST /api/admin/butterfly endpoint"""
        print("\n🧪 Testing POST /api/admin/butterfly...")
        
        # Test data as specified in the review request
        test_butterfly = {
            "commonName": "Test Butterfly",
            "latinName": "Testus butterflii", 
            "imageUrl": "https://example.com/test.jpg",
            "difficulty": 2
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/admin/butterfly",
                json=test_butterfly,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code != 200:
                self.test_results["admin_create_butterfly"]["details"] = f"HTTP {response.status_code}: {response.text}"
                self.test_results["overall"]["critical_issues"].append("admin create butterfly endpoint failed")
                print(f"❌ Admin create butterfly failed: {response.status_code}")
                return False
            
            created_butterfly = response.json()
            
            # Store the created butterfly ID for update/delete tests
            self.created_butterfly_id = created_butterfly.get("id")
            print(f"✅ Created butterfly with ID: {self.created_butterfly_id}")
            
            # Validate the created butterfly has all expected fields
            required_fields = ['id', 'commonName', 'latinName', 'imageUrl', 'difficulty']
            missing_fields = [field for field in required_fields if field not in created_butterfly]
            
            if missing_fields:
                self.test_results["admin_create_butterfly"]["details"] = f"Missing fields in response: {missing_fields}"
                self.test_results["overall"]["critical_issues"].append(f"Admin create response missing fields: {missing_fields}")
                print(f"❌ Missing fields in response: {missing_fields}")
                return False
            
            # Validate the data matches what we sent
            for field in ['commonName', 'latinName', 'imageUrl', 'difficulty']:
                if created_butterfly[field] != test_butterfly[field]:
                    self.test_results["admin_create_butterfly"]["details"] = f"Data mismatch in {field}"
                    self.test_results["overall"]["critical_issues"].append(f"Admin create data mismatch in {field}")
                    print(f"❌ Data mismatch: {field} = {created_butterfly[field]}, expected {test_butterfly[field]}")
                    return False
            
            print(f"✅ Data validation passed for created butterfly")
            
            self.test_results["admin_create_butterfly"]["passed"] = True
            self.test_results["admin_create_butterfly"]["details"] = f"Successfully created butterfly: {created_butterfly['commonName']}"
            return True
            
        except Exception as e:
            self.test_results["admin_create_butterfly"]["details"] = f"Exception: {str(e)}"
            self.test_results["overall"]["critical_issues"].append(f"admin create butterfly error: {str(e)}")
            print(f"❌ Admin create butterfly error: {e}")
            return False

    def test_admin_update_butterfly(self):
        """Test PUT /api/admin/butterfly/{id} endpoint"""
        print(f"\n🧪 Testing PUT /api/admin/butterfly/{self.created_butterfly_id}...")
        
        if not self.created_butterfly_id:
            self.test_results["admin_update_butterfly"]["details"] = "No butterfly ID available for update test"
            self.test_results["overall"]["critical_issues"].append("Cannot test update - no butterfly ID")
            print("❌ No butterfly ID available for update test")
            return False
        
        # Updated test data
        updated_butterfly = {
            "commonName": "Updated Test Butterfly",
            "latinName": "Testus butterflii updatus",
            "imageUrl": "https://example.com/updated-test.jpg", 
            "difficulty": 3
        }
        
        try:
            response = requests.put(
                f"{self.base_url}/admin/butterfly/{self.created_butterfly_id}",
                json=updated_butterfly,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code != 200:
                self.test_results["admin_update_butterfly"]["details"] = f"HTTP {response.status_code}: {response.text}"
                if response.status_code == 404:
                    self.test_results["overall"]["critical_issues"].append("admin update butterfly - butterfly not found")
                    print("❌ Butterfly not found for update")
                else:
                    self.test_results["overall"]["critical_issues"].append("admin update butterfly endpoint failed")
                    print(f"❌ Admin update butterfly failed: {response.status_code}")
                return False
            
            updated_result = response.json()
            print(f"✅ Updated butterfly with ID: {updated_result.get('id')}")
            
            # Validate the updated butterfly has all expected fields
            required_fields = ['id', 'commonName', 'latinName', 'imageUrl', 'difficulty']
            missing_fields = [field for field in required_fields if field not in updated_result]
            
            if missing_fields:
                self.test_results["admin_update_butterfly"]["details"] = f"Missing fields in response: {missing_fields}"
                self.test_results["overall"]["critical_issues"].append(f"Admin update response missing fields: {missing_fields}")
                print(f"❌ Missing fields in response: {missing_fields}")
                return False
            
            # Validate the data matches what we sent
            for field in ['commonName', 'latinName', 'imageUrl', 'difficulty']:
                if updated_result[field] != updated_butterfly[field]:
                    self.test_results["admin_update_butterfly"]["details"] = f"Data mismatch in {field}"
                    self.test_results["overall"]["critical_issues"].append(f"Admin update data mismatch in {field}")
                    print(f"❌ Data mismatch: {field} = {updated_result[field]}, expected {updated_butterfly[field]}")
                    return False
            
            print(f"✅ Update validation passed")
            
            self.test_results["admin_update_butterfly"]["passed"] = True
            self.test_results["admin_update_butterfly"]["details"] = f"Successfully updated butterfly: {updated_result['commonName']}"
            return True
            
        except Exception as e:
            self.test_results["admin_update_butterfly"]["details"] = f"Exception: {str(e)}"
            self.test_results["overall"]["critical_issues"].append(f"admin update butterfly error: {str(e)}")
            print(f"❌ Admin update butterfly error: {e}")
            return False

    def test_admin_delete_butterfly(self):
        """Test DELETE /api/admin/butterfly/{id} endpoint"""
        print(f"\n🧪 Testing DELETE /api/admin/butterfly/{self.created_butterfly_id}...")
        
        if not self.created_butterfly_id:
            self.test_results["admin_delete_butterfly"]["details"] = "No butterfly ID available for delete test"
            self.test_results["overall"]["critical_issues"].append("Cannot test delete - no butterfly ID")
            print("❌ No butterfly ID available for delete test")
            return False
        
        try:
            response = requests.delete(f"{self.base_url}/admin/butterfly/{self.created_butterfly_id}", timeout=10)
            
            if response.status_code != 200:
                self.test_results["admin_delete_butterfly"]["details"] = f"HTTP {response.status_code}: {response.text}"
                if response.status_code == 404:
                    self.test_results["overall"]["critical_issues"].append("admin delete butterfly - butterfly not found")
                    print("❌ Butterfly not found for deletion")
                else:
                    self.test_results["overall"]["critical_issues"].append("admin delete butterfly endpoint failed")
                    print(f"❌ Admin delete butterfly failed: {response.status_code}")
                return False
            
            result = response.json()
            print(f"✅ Delete response: {result.get('message', 'Butterfly deleted')}")
            
            # Verify the butterfly was actually deleted by checking the list
            print("🔍 Verifying butterfly was deleted...")
            get_response = requests.get(f"{self.base_url}/admin/butterflies", timeout=10)
            if get_response.status_code == 200:
                butterflies = get_response.json()
                deleted_butterfly = next((b for b in butterflies if b["id"] == self.created_butterfly_id), None)
                
                if deleted_butterfly is None:
                    print(f"✅ Verified: Butterfly {self.created_butterfly_id} is no longer in the list")
                else:
                    self.test_results["admin_delete_butterfly"]["details"] = "Butterfly still exists after deletion"
                    self.test_results["overall"]["critical_issues"].append("Admin delete - butterfly still exists after deletion")
                    print(f"❌ Butterfly {self.created_butterfly_id} still exists after deletion")
                    return False
            else:
                print("⚠️ Could not verify deletion - unable to retrieve butterfly list")
            
            self.test_results["admin_delete_butterfly"]["passed"] = True
            self.test_results["admin_delete_butterfly"]["details"] = f"Successfully deleted butterfly and verified removal"
            return True
            
        except Exception as e:
            self.test_results["admin_delete_butterfly"]["details"] = f"Exception: {str(e)}"
            self.test_results["overall"]["critical_issues"].append(f"admin delete butterfly error: {str(e)}")
            print(f"❌ Admin delete butterfly error: {e}")
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
        
        # Run tests in order - original endpoints first, then admin endpoints
        tests = [
            ("Initialize Butterflies", self.test_init_butterflies),
            ("Get All Butterflies", self.test_get_butterflies),
            ("Quiz Question", self.test_quiz_question),
            ("Admin Get Butterflies", self.test_admin_get_butterflies),
            ("Admin Create Butterfly", self.test_admin_create_butterfly),
            ("Admin Update Butterfly", self.test_admin_update_butterfly),
            ("Admin Delete Butterfly", self.test_admin_delete_butterfly)
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