#!/usr/bin/env python3
"""
Quick chatbot test to verify no authentication issues
"""

import requests
import json
import time

def test_chatbot_no_auth():
    """Test chatbot without any authentication"""
    
    base_url = "http://localhost:8000/api/v1"
    
    print("🤖 Testing Chatbot (No Authentication)")
    print("=" * 40)
    
    # Test 1: Health check
    print("1. Testing backend health...")
    try:
        response = requests.get("http://localhost:8000/healthz", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("Make sure the backend is running: cd backend && python main.py")
        return False
    
    # Test 2: Create chat session (no auth)
    print("\n2. Testing chat session creation (no auth)...")
    session_data = {
        "fraud_type": "general_security",
        "vulnerability_factors": []
    }
    
    try:
        response = requests.post(
            f"{base_url}/chatbot/sessions",
            json=session_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
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
    
    # Test 3: Send message (no auth)
    print("\n3. Testing message sending (no auth)...")
    message_data = {
        "content": "Hello! Can you help me with cybersecurity?",
        "metadata": {"test": True}
    }
    
    try:
        print("Sending message...")
        response = requests.post(
            f"{base_url}/chatbot/sessions/{session_id}/messages",
            json=message_data,
            headers={"Content-Type": "application/json"},
            timeout=30  # Longer timeout for AI response
        )
        
        print(f"Status Code: {response.status_code}")
        
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
    
    # Test 4: Get messages (no auth)
    print("\n4. Testing message retrieval (no auth)...")
    try:
        response = requests.get(f"{base_url}/chatbot/sessions/{session_id}/messages", timeout=10)
        
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

def test_frontend_access():
    """Test if frontend is accessible"""
    print("\n🌐 Testing Frontend Access")
    print("=" * 30)
    
    try:
        response = requests.get("http://localhost:5173", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            print("   Go to: http://localhost:5173")
            return True
        else:
            print(f"❌ Frontend not accessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend not running: {e}")
        print("Start frontend with: npm run dev")
        return False

if __name__ == "__main__":
    print("🚀 Quick Chatbot Test (No Authentication)")
    print("=" * 50)
    
    # Test backend chatbot
    backend_success = test_chatbot_no_auth()
    
    # Test frontend access
    frontend_success = test_frontend_access()
    
    print("\n🎉 Test Summary:")
    print("=" * 20)
    print(f"✅ Backend Chatbot: {'Working' if backend_success else 'Failed'}")
    print(f"✅ Frontend Access: {'Working' if frontend_success else 'Failed'}")
    
    if backend_success and frontend_success:
        print("\n🎉 Everything is working! The chatbot is ready to use.")
        print("\n📋 Next Steps:")
        print("1. Go to: http://localhost:5173")
        print("2. Start chatting with the AI security advisor")
        print("3. No authentication required!")
        print("\n💡 Test Messages:")
        print("- 'How can I identify phishing emails?'")
        print("- 'What are signs of a romance scam?'")
        print("- 'Help me understand investment fraud'")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
        print("\n🔧 Troubleshooting:")
        if not backend_success:
            print("1. Start backend: cd backend && python main.py")
            print("2. Check HF_TOKEN is set")
            print("3. Run: python init_db.py")
        if not frontend_success:
            print("4. Start frontend: npm run dev")
            print("5. Check if port 5173 is available")
