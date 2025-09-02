#!/usr/bin/env python3
"""
VulnLib Vulnerability Test Suite
Tests various security vulnerabilities for educational purposes
"""

import requests
import json
import time

BASE_URL = 'http://localhost:5000'

def test_reflected_xss():
    """Test reflected XSS in search functionality"""
    print("🔍 Testing Reflected XSS...")
    
    xss_payload = '<script>alert("XSS")</script>'
    response = requests.get(f'{BASE_URL}/search?q={xss_payload}')
    
    if xss_payload in response.text:
        print("✅ Reflected XSS vulnerability confirmed")
        return True
    else:
        print("❌ Reflected XSS not found")
        return False

def test_username_enumeration():
    """Test username enumeration via timing attack"""
    print("👤 Testing Username Enumeration...")
    
    # Test with existing user
    start_time = time.time()
    response1 = requests.post(f'{BASE_URL}/api/auth/login', 
                             json={'username': 'admin', 'password': 'wrongpassword'})
    time1 = time.time() - start_time
    
    # Test with non-existing user  
    start_time = time.time()
    response2 = requests.post(f'{BASE_URL}/api/auth/login',
                             json={'username': 'nonexistentuser', 'password': 'wrongpassword'})
    time2 = time.time() - start_time
    
    time_diff = abs(time1 - time2)
    
    if time_diff > 0.2:  # Significant timing difference
        print(f"✅ Username enumeration possible (timing diff: {time_diff:.2f}s)")
        print(f"   Existing user response: {response1.json().get('message', '')}")
        print(f"   Non-existing user response: {response2.json().get('message', '')}")
        return True
    else:
        print("❌ No significant timing difference found")
        return False

def test_idor():
    """Test IDOR vulnerability"""
    print("🔐 Testing IDOR (Insecure Direct Object Reference)...")
    
    # Try to access another user's data without authentication
    response = requests.get(f'{BASE_URL}/api/users/any-uuid/loans')
    
    if response.status_code != 401:  # Should require authentication but doesn't
        print("✅ IDOR vulnerability confirmed - accessing user data without auth")
        return True
    else:
        print("❌ IDOR test inconclusive - requires authentication")
        return False

def test_stored_xss_setup():
    """Test stored XSS by creating a review with XSS payload"""
    print("💾 Testing Stored XSS in Reviews...")
    
    xss_payload = '<script>alert("Stored XSS")</script>'
    
    # Get first book
    books_response = requests.get(f'{BASE_URL}/api/books')
    if books_response.status_code == 200:
        books = books_response.json().get('books', [])
        if books:
            book_id = books[0]['id']
            
            # Create review with XSS payload
            review_data = {
                'user_id': 'test-user-id',
                'rating': 5,
                'comment': xss_payload
            }
            
            response = requests.post(f'{BASE_URL}/api/books/{book_id}/reviews',
                                   json=review_data)
            
            if response.status_code == 200:
                print("✅ Stored XSS payload submitted successfully")
                print(f"   Check book reviews at: {BASE_URL}/books/{book_id}")
                return True
            else:
                print(f"❌ Failed to submit review: {response.status_code}")
                return False
    
    print("❌ Could not get books for XSS test")
    return False

def test_sql_injection():
    """Test SQL injection in reports endpoint"""
    print("💉 Testing SQL Injection...")
    
    # Try SQL injection payload
    sql_payload = "1' UNION SELECT 1,2,3,4,5,6,7,8--"
    
    response = requests.get(f'{BASE_URL}/api/reports/loans?year=2024&month={sql_payload}')
    
    if 'error' in response.text.lower() or 'sql' in response.text.lower():
        print("✅ SQL Injection vulnerability likely present")
        print(f"   Response: {response.text[:200]}...")
        return True
    elif response.status_code == 500:
        print("✅ SQL Injection caused server error")
        return True
    else:
        print("❌ No clear SQL injection indication")
        return False

def test_open_redirect():
    """Test open redirect vulnerability"""
    print("🔀 Testing Open Redirect...")
    
    malicious_url = "http://evil.com"
    response = requests.get(f'{BASE_URL}/books/any-id?next={malicious_url}', 
                           allow_redirects=False)
    
    if malicious_url in response.text:
        print("✅ Open redirect vulnerability confirmed")
        return True
    else:
        print("❌ Open redirect not confirmed")
        return False

def test_file_upload():
    """Test unrestricted file upload"""
    print("📁 Testing File Upload...")
    
    # Try to upload a potentially malicious file
    files = {'file': ('test.php', '<?php echo "Uploaded PHP file"; ?>', 'text/plain')}
    
    response = requests.post(f'{BASE_URL}/api/books/any-id/upload', files=files)
    
    if response.status_code != 401:  # Should require auth but might not
        if 'success' in response.text.lower():
            print("✅ File upload vulnerability confirmed")
            return True
        else:
            print("⚠️  File upload endpoint accessible but failed")
            return False
    else:
        print("❌ File upload requires authentication")
        return False

def test_business_logic():
    """Test business logic flaws"""
    print("🧠 Testing Business Logic Flaws...")
    
    # Test self-approval of loans (should not be possible)
    loan_data = {'status': 'approved'}
    response = requests.put(f'{BASE_URL}/api/loans/any-loan-id/approve', 
                           json=loan_data)
    
    if response.status_code != 401:  # Should require proper authorization
        print("✅ Business logic flaw - loan self-approval possible")
        return True
    else:
        print("❌ Business logic test requires authentication")
        return False

def main():
    """Run all vulnerability tests"""
    print("🚀 Starting VulnLib Vulnerability Test Suite")
    print("=" * 50)
    
    tests = [
        test_reflected_xss,
        test_username_enumeration, 
        test_idor,
        test_stored_xss_setup,
        test_sql_injection,
        test_open_redirect,
        test_file_upload,
        test_business_logic
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print("-" * 30)
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            print("-" * 30)
    
    print(f"\n🎯 Test Results: {passed}/{total} vulnerabilities confirmed")
    
    if passed >= total * 0.7:  # 70% or more
        print("✅ VulnLib is ready for penetration testing education!")
    else:
        print("⚠️  Some vulnerabilities may not be accessible without authentication")
    
    print("\n⚠️  Remember: These are intentional vulnerabilities for education only!")
    print("🔒 Never use these patterns in production applications!")

if __name__ == '__main__':
    main()