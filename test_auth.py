#!/usr/bin/env python3
"""
Test script for authentication endpoints
This script tests the login functionality to identify issues
"""

import requests
import json
import sys

def test_auth_endpoints():
    """Test the authentication endpoints"""
    
    base_url = "http://localhost:8000/api/v1"
    
    print("🔐 Testing Authentication Endpoints")
    print("=" * 40)
    
    # Test 1: Health check
    print("1. Testing health check...")
    try:
        response = requests.get("http://localhost:8000/healthz")
        if response.status_code == 200:
            print("✅ Backend is running")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("Make sure the backend is running on http://localhost:8000")
        return False
    
    # Test 2: Login with demo credentials
    print("\n2. Testing login with demo credentials...")
    login_data = {
        "email": "demo@example.com",
        "password": "demo123"
    }
    
    try:
        response = requests.post(
            f"{base_url}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful!")
            print(f"   Token: {data.get('access_token', 'N/A')[:20]}...")
            print(f"   User ID: {data.get('user_id', 'N/A')}")
            print(f"   Email: {data.get('email', 'N/A')}")
            return data.get('access_token')
        else:
            print(f"❌ Login failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Login request failed: {e}")
        return False
    
    # Test 3: Test protected endpoint
    print("\n3. Testing protected endpoint...")
    if token:
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{base_url}/auth/me", headers=headers)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                print("✅ Protected endpoint access successful!")
            else:
                print(f"❌ Protected endpoint access failed: {response.text}")
                
        except Exception as e:
            print(f"❌ Protected endpoint request failed: {e}")

def test_chatbot_endpoints(token):
    """Test chatbot endpoints"""
    
    base_url = "http://localhost:8000/api/v1"
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n🤖 Testing Chatbot Endpoints")
    print("=" * 40)
    
    # Test 1: Create chat session
    print("1. Testing chat session creation...")
    try:
        session_data = {
            "fraud_type": "general_security",
            "vulnerability_factors": []
        }
        
        response = requests.post(
            f"{base_url}/chatbot/sessions",
            json=session_data,
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            session_id = data.get('session_id')
            print(f"✅ Chat session created: {session_id}")
            return session_id
        else:
            print(f"❌ Chat session creation failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Chat session request failed: {e}")
        return None
    
    # Test 2: Send message
    if session_id:
        print("\n2. Testing message sending...")
        try:
            message_data = {
                "content": "Hello, I need help with cybersecurity",
                "metadata": {"test": True}
            }
            
            response = requests.post(
                f"{base_url}/chatbot/sessions/{session_id}/messages",
                json=message_data,
                headers=headers
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                print("✅ Message sent successfully!")
            else:
                print(f"❌ Message sending failed: {response.text}")
                
        except Exception as e:
            print(f"❌ Message request failed: {e}")

if __name__ == "__main__":
    print("🚀 Starting Authentication and Chatbot Tests")
    print("=" * 50)
    
    # Test authentication
    token = test_auth_endpoints()
    
    if token:
        # Test chatbot endpoints
        session_id = test_chatbot_endpoints(token)
        
        print("\n🎉 Test Summary:")
        print("=" * 20)
        print("✅ Authentication: Working")
        print("✅ Chatbot Integration: Working" if session_id else "❌ Chatbot Integration: Failed")
    else:
        print("\n❌ Test Summary:")
        print("=" * 20)
        print("❌ Authentication: Failed")
        print("❌ Chatbot Integration: Not tested")
    
    print("\nIf tests failed, check:")
    print("1. Backend is running: python main.py")
    print("2. Database is initialized")
    print("3. All dependencies are installed")
    print("4. HF_TOKEN is set in environment")
