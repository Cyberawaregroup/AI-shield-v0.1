import logging
from typing import Any, Dict, List, Optional
import uuid

from app.db.types import FraudType, RiskLevel
from app.services.huggingface_service import HuggingFaceService
from app.services.threat_intelligence import ThreatIntelligenceService

logger = logging.getLogger(__name__)


class ChatbotService:
    """Service for managing AI-powered fraud advice chatbot"""

    def __init__(
        self,
        huggingface_service: HuggingFaceService,
        threat_service: ThreatIntelligenceService,
    ):
        self.huggingface_service = huggingface_service
        self.threat_service = threat_service

        # Predefined responses for common scenarios
        self.common_responses = {
            "greeting": "Hello! I'm your AI security advisor. I can help you with fraud detection, security advice, and threat assessment. What security concern would you like to discuss today?",
            "phishing_suspicion": "I understand you're concerned about a potential phishing attempt. This is a common and serious threat. Let me help you assess the situation. Can you tell me more about what you received?",
            "romance_scam": "Romance scams can be emotionally devastating and financially damaging. I'm here to help you evaluate the situation objectively. What specific behaviors or requests have raised your concerns?",
            "investment_scam": "Investment scams often promise unrealistic returns and use high-pressure tactics. Let me help you identify the warning signs. What investment opportunity are you considering?",
            "tech_support": "Tech support scams are increasingly sophisticated. They often claim to be from well-known companies. What company are they claiming to represent, and what problem are they saying you have?",
            "elderly_vulnerability": "I understand this situation may be particularly concerning. Elderly individuals are often targeted by scammers. Let me provide you with extra support and guidance.",
            "high_risk": "This situation appears to be high-risk. I recommend we escalate this to a human security advisor who can provide immediate assistance. Would you like me to do that now?",
        }

    def generate_session_id(self) -> str:
        """Generate a unique session ID"""
        return f"chat_{uuid.uuid4().hex[:8]}"

    async def generate_initial_response(
        self,
        initial_message: str,
        fraud_type: Optional[FraudType] = None,
        vulnerability_factors: List[str] | None = None,
    ) -> Dict[str, Any]:
        """
        Generate the initial AI response for a new chat session

        Args:
            initial_message: User's first message
            fraud_type: Type of fraud being discussed
            vulnerability_factors: Factors that make the user vulnerable

        Returns:
            Dictionary containing AI response and metadata
        """
        try:
            # Analyze the initial message for fraud type and risk level
            analysis = await self._analyze_message(
                initial_message, fraud_type, vulnerability_factors
            )

            # Generate appropriate response
            if analysis["risk_level"] == RiskLevel.CRITICAL:
                response = self.common_responses["high_risk"]
                escalate = True
                escalation_reason = "Critical risk level detected in initial message"
            elif analysis["risk_level"] == RiskLevel.HIGH:
                response = self.common_responses.get(
                    analysis["fraud_type"], self.common_responses["greeting"]
                )
                escalate = False
                escalation_reason = None
            else:
                response = self.common_responses["greeting"]
                escalate = False
                escalation_reason = None

            # Add vulnerability-specific guidance
            if vulnerability_factors and "elderly" in vulnerability_factors:
                response += "\n\n" + self.common_responses["elderly_vulnerability"]

            return {
                "content": response,
                "metadata": {
                    "fraud_type": analysis["fraud_type"],
                    "risk_level": analysis["risk_level"],
                    "confidence": analysis["confidence"],
                    "escalate": escalate,
                    "escalation_reason": escalation_reason,
                },
                "ai_model": "gpt-4o",
                "ai_confidence": analysis["confidence"],
            }

        except Exception as e:
            logger.error(f"Error generating initial response: {str(e)}")
            return {
                "content": self.common_responses["greeting"],
                "metadata": {"error": str(e)},
                "ai_model": "fallback",
                "ai_confidence": 0.0,
            }

    async def generate_response(
        self, user_message: str, session_context: Dict[str, Any], user_id: int
    ) -> Dict[str, Any]:
        """
        Generate AI response based on user message and session context

        Args:
            user_message: User's message
            session_context: Current session context
            user_id: ID of the user

        Returns:
            Dictionary containing AI response and metadata
        """
        try:
            # Analyze the message for risk assessment
            risk_analysis = await self._analyze_message(
                user_message, session_context.get("fraud_type")
            )

            # Check if escalation is needed
            if risk_analysis["risk_level"] in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
                escalation_needed = True
                escalation_reason = f"High risk detected: {risk_analysis['risk_level']}"
            else:
                escalation_needed = False
                escalation_reason = None

            # Generate AI response
            if self.huggingface_service.is_available():
                ai_response = await self.huggingface_service.generate_fraud_advice(
                    user_message, session_context, risk_analysis
                )
                response_content = ai_response["content"]
                ai_confidence = ai_response.get("confidence", 0.8)
            else:
                # Fallback to rule-based response
                response_content = self._generate_fallback_response(
                    user_message, risk_analysis
                )
                ai_confidence = 0.5

            return {
                "content": response_content,
                "metadata": {
                    "risk_level": risk_analysis["risk_level"],
                    "fraud_type": risk_analysis["fraud_type"],
                    "confidence": ai_confidence,
                    "escalation_needed": escalation_needed,
                    "escalation_reason": escalation_reason,
                    "ai_model": "gpt-4o"
                    if self.openai_service.is_available()
                    else "fallback",
                },
                "ai_confidence": ai_confidence,
            }

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return {
                "content": "I'm sorry, I'm experiencing technical difficulties. Please try again or contact a human advisor.",
                "metadata": {"error": str(e)},
                "ai_model": "fallback",
                "ai_confidence": 0.0,
            }

    async def escalate_session(
        self, session_id: int, reason: str, priority: str = "normal"
    ) -> bool:
        """
        Escalate a chat session to a human advisor

        Args:
            session_id: ID of the chat session
            reason: Reason for escalation
            priority: Priority level for the escalation

        Returns:
            True if escalation successful, False otherwise
        """
        try:
            # This would typically involve:
            # 1. Updating session status
            # 2. Notifying available advisors
            # 3. Assigning to appropriate advisor
            # 4. Sending escalation notification

            logger.info(
                f"Session {session_id} escalated: {reason} (Priority: {priority})"
            )
            return True

        except Exception as e:
            logger.error(f"Error escalating session {session_id}: {str(e)}")
            return False

    async def _analyze_message(
        self,
        message: str,
        fraud_type: Optional[FraudType] = None,
        vulnerability_factors: List[str] | None = None,
    ) -> Dict[str, Any]:
        """
        Analyze a message for fraud type and risk level

        Args:
            message: Message to analyze
            fraud_type: Known fraud type if available
            vulnerability_factors: User vulnerability factors

        Returns:
            Dictionary with analysis results
        """
        try:
            message_lower = message.lower()

            # Determine fraud type if not provided
            if not fraud_type:
                if any(
                    word in message_lower
                    for word in ["phish", "email", "link", "click"]
                ):
                    fraud_type = FraudType.PHISHING
                elif any(
                    word in message_lower
                    for word in ["romance", "love", "relationship", "dating"]
                ):
                    fraud_type = FraudType.ROMANCE_SCAM
                elif any(
                    word in message_lower
                    for word in ["invest", "money", "profit", "return"]
                ):
                    fraud_type = FraudType.INVESTMENT_SCAM
                elif any(
                    word in message_lower
                    for word in ["tech", "support", "computer", "virus"]
                ):
                    fraud_type = FraudType.TECH_SUPPORT_SCAM
                elif any(
                    word in message_lower
                    for word in ["bank", "account", "card", "payment"]
                ):
                    fraud_type = FraudType.BANKING_SCAM
                else:
                    fraud_type = FraudType.OTHER

            # Assess risk level
            risk_level = RiskLevel.LOW

            # High-risk keywords
            high_risk_words = [
                "urgent",
                "immediate",
                "now",
                "limited time",
                "act fast",
                "don't tell anyone",
            ]
            if any(word in message_lower for word in high_risk_words):
                risk_level = RiskLevel.HIGH

            # Critical risk indicators
            critical_words = [
                "bank transfer",
                "gift cards",
                "bitcoin",
                "crypto",
                "social security",
            ]
            if any(word in message_lower for word in critical_words):
                risk_level = RiskLevel.CRITICAL

            # Adjust based on vulnerability factors
            if vulnerability_factors:
                if "elderly" in vulnerability_factors:
                    if risk_level == RiskLevel.LOW:
                        risk_level = RiskLevel.MEDIUM
                    elif risk_level == RiskLevel.MEDIUM:
                        risk_level = RiskLevel.HIGH
                if "recent_stress" in vulnerability_factors:
                    if risk_level == RiskLevel.LOW:
                        risk_level = RiskLevel.MEDIUM

            # Calculate confidence score
            confidence = 0.7  # Base confidence
            if fraud_type != FraudType.OTHER:
                confidence += 0.2
            if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
                confidence += 0.1

            return {
                "fraud_type": fraud_type,
                "risk_level": risk_level,
                "confidence": min(confidence, 1.0),
                "keywords_found": [
                    word
                    for word in high_risk_words + critical_words
                    if word in message_lower
                ],
            }

        except Exception as e:
            logger.error(f"Error analyzing message: {str(e)}")
            return {
                "fraud_type": FraudType.OTHER,
                "risk_level": RiskLevel.LOW,
                "confidence": 0.5,
                "error": str(e),
            }

    def _generate_fallback_response(
        self, message: str, analysis: Dict[str, Any]
    ) -> str:
        """
        Generate a fallback response when AI service is unavailable

        Args:
            message: User's message
            analysis: Risk analysis results

        Returns:
            Fallback response text
        """
        fraud_type = analysis.get("fraud_type", FraudType.OTHER)
        risk_level = analysis.get("risk_level", RiskLevel.LOW)

        if risk_level == RiskLevel.CRITICAL:
            return "This situation requires immediate attention. I'm escalating you to a human security advisor right now."
        elif risk_level == RiskLevel.HIGH:
            return f"I'm concerned about this {fraud_type} situation. Let me provide you with some immediate safety steps while we get you connected to a human advisor."
        elif risk_level == RiskLevel.MEDIUM:
            return f"This {fraud_type} situation has some concerning elements. Let me help you assess the risks and provide guidance."
        else:
            return f"I understand your concern about {fraud_type}. Let me help you evaluate this situation and provide security advice."
