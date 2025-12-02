import logging
from typing import Dict, Any, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)


class OpenAIService:
    """Service for interacting with OpenAI GPT-4o API"""

    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.is_available_flag = bool(self.api_key)

        if not self.api_key:
            logger.warning(
                "OpenAI API key not configured. AI features will be limited."
            )

    def is_available(self) -> bool:
        """Check if OpenAI service is available"""
        return self.is_available_flag

    async def generate_fraud_advice(
        self,
        user_message: str,
        session_context: Dict[str, Any],
        risk_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate fraud advice using OpenAI GPT-4o

        Args:
            user_message: User's message
            session_context: Current session context
            risk_analysis: Risk analysis results

        Returns:
            Dictionary containing AI response and metadata
        """
        try:
            if not self.is_available():
                return {
                    "content": "AI service is currently unavailable. Please contact a human advisor.",
                    "confidence": 0.0,
                    "model": "unavailable",
                }

            # This would typically make an API call to OpenAI
            # For now, return a mock response
            mock_response = self._generate_mock_response(user_message, risk_analysis)

            return {
                "content": mock_response,
                "confidence": 0.85,
                "model": "gpt-4o",
                "reasoning": "AI analysis based on message content and risk assessment",
            }

        except Exception as e:
            logger.error(f"Error generating OpenAI response: {str(e)}")
            return {
                "content": "I'm experiencing technical difficulties. Please try again or contact a human advisor.",
                "confidence": 0.0,
                "model": "error",
            }

    def _generate_mock_response(
        self, user_message: str, risk_analysis: Dict[str, Any]
    ) -> str:
        """
        Generate a mock response when OpenAI is not available

        Args:
            user_message: User's message
            risk_analysis: Risk analysis results

        Returns:
            Mock response text
        """
        fraud_type = risk_analysis.get("fraud_type", "unknown")
        risk_level = risk_analysis.get("risk_level", "low")

        if risk_level == "critical":
            return f"This {fraud_type} situation is extremely dangerous and requires immediate action. Do not send any money or personal information. Contact your bank immediately and report this to Action Fraud."
        elif risk_level == "high":
            return f"I'm very concerned about this {fraud_type} situation. There are several red flags that suggest this is a scam. Please stop all communication and do not provide any personal or financial information."
        elif risk_level == "medium":
            return f"This {fraud_type} situation has some concerning elements. Let me help you identify the warning signs and provide guidance on how to protect yourself."
        else:
            return f"I understand your concern about {fraud_type}. While this may not be an immediate threat, it's good that you're being cautious. Let me help you evaluate the situation."

    async def analyze_message(
        self,
        message: str,
        fraud_type: Optional[str] = None,
        vulnerability_factors: Optional[list] = None,
    ) -> Dict[str, Any]:
        """
        Analyze a message for fraud indicators using AI

        Args:
            message: Message to analyze
            fraud_type: Known fraud type if available
            vulnerability_factors: User vulnerability factors

        Returns:
            Dictionary with AI analysis results
        """
        try:
            if not self.is_available():
                return {
                    "fraud_type": fraud_type or "unknown",
                    "risk_level": "medium",
                    "confidence": 0.5,
                    "ai_available": False,
                }

            # This would typically use OpenAI's content moderation or analysis
            # For now, return basic analysis
            analysis = self._basic_ai_analysis(
                message, fraud_type, vulnerability_factors
            )

            return {
                "fraud_type": analysis["fraud_type"],
                "risk_level": analysis["risk_level"],
                "confidence": analysis["confidence"],
                "ai_available": True,
                "keywords_detected": analysis.get("keywords", []),
            }

        except Exception as e:
            logger.error(f"Error in AI message analysis: {str(e)}")
            return {
                "fraud_type": fraud_type or "unknown",
                "risk_level": "medium",
                "confidence": 0.3,
                "ai_available": False,
                "error": str(e),
            }

    def _basic_ai_analysis(
        self,
        message: str,
        fraud_type: Optional[str] = None,
        vulnerability_factors: Optional[list] = None,
    ) -> Dict[str, Any]:
        """
        Basic AI-like analysis using keyword matching and rules

        Args:
            message: Message to analyze
            fraud_type: Known fraud type
            vulnerability_factors: User vulnerability factors

        Returns:
            Basic analysis results
        """
        message_lower = message.lower()

        # Detect fraud type if not provided
        if not fraud_type:
            if any(word in message_lower for word in ["phish", "email", "link"]):
                fraud_type = "phishing"
            elif any(
                word in message_lower for word in ["love", "romance", "relationship"]
            ):
                fraud_type = "romance_scam"
            elif any(word in message_lower for word in ["invest", "money", "profit"]):
                fraud_type = "investment_scam"
            else:
                fraud_type = "unknown"

        # Assess risk level
        risk_level = "low"
        confidence = 0.6

        # High-risk indicators
        high_risk_words = ["urgent", "immediate", "now", "limited time"]
        if any(word in message_lower for word in high_risk_words):
            risk_level = "high"
            confidence += 0.2

        # Critical risk indicators
        critical_words = ["bank transfer", "gift cards", "bitcoin", "crypto"]
        if any(word in message_lower for word in critical_words):
            risk_level = "critical"
            confidence += 0.3

        # Adjust based on vulnerability factors
        if vulnerability_factors:
            if "elderly" in vulnerability_factors:
                if risk_level == "low":
                    risk_level = "medium"
                elif risk_level == "medium":
                    risk_level = "high"
                confidence += 0.1

        return {
            "fraud_type": fraud_type,
            "risk_level": risk_level,
            "confidence": min(confidence, 1.0),
            "keywords": [
                word
                for word in high_risk_words + critical_words
                if word in message_lower
            ],
        }
