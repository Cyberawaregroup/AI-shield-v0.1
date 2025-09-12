#!/usr/bin/env python3
"""
Test script for HuggingFace chatbot integration
This script tests the cybersecurity chatbot with various phishing and scam scenarios
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.services.huggingface_service import HuggingFaceService
from app.core.config import settings

async def test_chatbot():
    """Test the HuggingFace chatbot service with various scenarios"""
    
    print("🤖 Testing HuggingFace Cybersecurity Chatbot")
    print("=" * 50)
    
    # Set the HF token
    os.environ["HF_TOKEN"] = "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"
    
    # Initialize the service
    hf_service = HuggingFaceService()
    
    if not hf_service.is_available():
        print("❌ HuggingFace service is not available. Check your token.")
        return
    
    print("✅ HuggingFace service initialized successfully")
    print()
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Phishing Email Suspicion",
            "message": "I received an email from my bank asking me to click a link to verify my account. The email looks urgent and says my account will be suspended if I don't act immediately.",
            "fraud_type": "phishing",
            "vulnerability_factors": []
        },
        {
            "name": "Romance Scam Warning",
            "message": "I've been talking to someone online for months. They say they love me and want to meet, but they keep asking for money to help with emergencies. They're in another country.",
            "fraud_type": "romance_scam",
            "vulnerability_factors": ["elderly"]
        },
        {
            "name": "Investment Scam Alert",
            "message": "Someone contacted me about a guaranteed investment opportunity with 300% returns. They want me to send Bitcoin to get started. It sounds too good to be true.",
            "fraud_type": "investment_scam",
            "vulnerability_factors": []
        },
        {
            "name": "Tech Support Scam",
            "message": "I got a call saying my computer has a virus and they need remote access to fix it. They're asking for my credit card information to process the fix.",
            "fraud_type": "tech_support",
            "vulnerability_factors": []
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"📋 Test {i}: {scenario['name']}")
        print(f"User Message: {scenario['message']}")
        print()
        
        # Analyze the message
        risk_analysis = await hf_service.analyze_message(
            scenario['message'],
            scenario['fraud_type'],
            scenario['vulnerability_factors']
        )
        
        print(f"🔍 Risk Analysis:")
        print(f"   Fraud Type: {risk_analysis['fraud_type']}")
        print(f"   Risk Level: {risk_analysis['risk_level']}")
        print(f"   Confidence: {risk_analysis['confidence']:.2f}")
        if 'warning_signs' in risk_analysis:
            print(f"   Warning Signs: {', '.join(risk_analysis['warning_signs'])}")
        print()
        
        # Generate advice
        session_context = {
            "fraud_type": scenario['fraud_type'],
            "vulnerability_factors": scenario['vulnerability_factors']
        }
        
        advice = await hf_service.generate_fraud_advice(
            scenario['message'],
            session_context,
            risk_analysis
        )
        
        print(f"🛡️ Cybersecurity Advice:")
        print(f"   {advice['content']}")
        print(f"   Confidence: {advice['confidence']:.2f}")
        print(f"   Model: {advice['model']}")
        print()
        print("-" * 50)
        print()
    
    print("✅ All tests completed!")

if __name__ == "__main__":
    asyncio.run(test_chatbot())
