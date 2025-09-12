#!/usr/bin/env python3
"""
Simple chatbot test script (No authentication required)
This script tests the chatbot functionality with HuggingFace integration
"""

import requests
import json
import sys

def test_chatbot():
    """Test the chatbot endpoints without authentication"""
    
    base_url = "http://localhost:8000/api/v1"
    
    print("🤖 Testing Chatbot (No Auth Required)")
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
    
    # Test 2: Create chat session
    print("\n2. Testing chat session creation...")
    session_data = {
        "fraud_type": "general_security",
        "vulnerability_factors": []
    }
    
    try:
        response = requests.post(
            f"{base_url}/chatbot/sessions",
            json=session_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            session_id = data.get('session_id')
            print(f"✅ Chat session created: {session_id}")
        else:
            print(f"❌ Chat session creation failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Chat session request failed: {e}")
        return False
    
    # Test 3: Send message
    print("\n3. Testing message sending...")
    message_data = {
        "content": "Hello, I need help with cybersecurity. Can you help me identify phishing emails?",
        "metadata": {"test": True}
    }
    
    try:
        response = requests.post(
            f"{base_url}/chatbot/sessions/{session_id}/messages",
            json=message_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Message sent successfully!")
            print(f"   AI Response: {data.get('content', 'N/A')[:100]}...")
            print(f"   AI Model: {data.get('ai_model', 'N/A')}")
            print(f"   Confidence: {data.get('ai_confidence', 'N/A')}")
        else:
            print(f"❌ Message sending failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Message request failed: {e}")
        return False
    
    # Test 4: Get chat messages
    print("\n4. Testing message retrieval...")
    try:
        response = requests.get(f"{base_url}/chatbot/sessions/{session_id}/messages")
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            messages = response.json()
            print(f"✅ Retrieved {len(messages)} messages")
            for i, msg in enumerate(messages):
                print(f"   Message {i+1}: {msg.get('message_type', 'unknown')} - {msg.get('content', 'N/A')[:50]}...")
        else:
            print(f"❌ Message retrieval failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Message retrieval request failed: {e}")
    
    return True

def test_huggingface_service():
    """Test if HuggingFace service is working"""
    
    print("\n🔍 Testing HuggingFace Service")
    print("=" * 30)
    
    try:
        # Test a simple message
        message_data = {
            "content": "What are the signs of a phishing email?",
            "metadata": {"test": True}
        }
        
        # Create a session first
        session_response = requests.post(
            "http://localhost:8000/api/v1/chatbot/sessions",
            json={"fraud_type": "phishing", "vulnerability_factors": []},
            headers={"Content-Type": "application/json"}
        )
        
        if session_response.status_code != 200:
            print("❌ Failed to create session for HF test")
            return False
        
        session_id = session_response.json().get('session_id')
        
        # Send message
        response = requests.post(
            f"http://localhost:8000/api/v1/chatbot/sessions/{session_id}/messages",
            json=message_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ HuggingFace service is working!")
            print(f"   Response: {data.get('content', 'N/A')[:100]}...")
            print(f"   Model: {data.get('ai_model', 'N/A')}")
            return True
        else:
            print(f"❌ HuggingFace service failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ HuggingFace test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Simple Chatbot Tests")
    print("=" * 50)
    
    # Test basic chatbot functionality
    chatbot_success = test_chatbot()
    
    # Test HuggingFace integration
    hf_success = test_huggingface_service()
    
    print("\n🎉 Test Summary:")
    print("=" * 20)
    print(f"✅ Basic Chatbot: {'Working' if chatbot_success else 'Failed'}")
    print(f"✅ HuggingFace AI: {'Working' if hf_success else 'Failed'}")
    
    if chatbot_success and hf_success:
        print("\n🎉 All tests passed! The chatbot is ready to use.")
        print("\nTo use the chatbot:")
        print("1. Start backend: cd backend && python main.py")
        print("2. Start frontend: npm run dev")
        print("3. Go to: http://localhost:5173")
        print("4. Start chatting with the AI security advisor!")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
        print("\nTroubleshooting:")
        print("1. Make sure backend is running: python main.py")
        print("2. Check HF_TOKEN is set in environment")
        print("3. Verify database is initialized")
        print("4. Check backend logs for errors")
