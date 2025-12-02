import logging
from typing import Dict, Any, Optional
from huggingface_hub import InferenceClient
from app.core.config import settings

logger = logging.getLogger(__name__)


class HuggingFaceService:
    """Service for interacting with Hugging Face Inference API using GPT-OSS models"""

    def __init__(self):
        self.api_key = settings.HF_TOKEN
        self.is_available_flag = bool(self.api_key)

        if not self.api_key:
            logger.warning(
                "Hugging Face API token not configured. AI features will be limited."
            )
        else:
            try:
                self.client = InferenceClient(token=self.api_key)
                logger.info("Hugging Face Inference client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Hugging Face client: {str(e)}")
                self.is_available_flag = False

    def is_available(self) -> bool:
        """Check if Hugging Face service is available"""
        return self.is_available_flag

    def _get_cybersecurity_system_prompt(self) -> str:
        """
        Comprehensive cybersecurity system prompt focused on phishing and scam awareness
        """
        return """You are an expert cybersecurity advisor and fraud prevention specialist. Your primary mission is to protect users from phishing attacks, scams, and online fraud. You have extensive knowledge of:

**Core Expertise:**
- Phishing detection and prevention
- Romance scams and catfishing
- Investment and cryptocurrency scams
- Tech support scams
- Identity theft prevention
- Social engineering tactics
- Email security and verification
- Website safety assessment
- Financial fraud patterns

**Your Approach:**
1. **Immediate Risk Assessment**: Always prioritize user safety and financial protection
2. **Educational Focus**: Explain threats clearly and help users understand warning signs
3. **Actionable Guidance**: Provide specific steps users can take to protect themselves
4. **Empathetic Support**: Be understanding while maintaining urgency for serious threats
5. **Evidence-Based Analysis**: Look for specific red flags and suspicious patterns

**Key Warning Signs You Identify:**
- Urgent requests for money or personal information
- Requests for gift cards, wire transfers, or cryptocurrency
- Suspicious email addresses or domains
- Poor grammar and spelling in official communications
- Requests to keep communications secret
- Pressure tactics and artificial urgency
- Unsolicited contact claiming to be from trusted organizations
- Requests for remote access to devices
- Investment opportunities with guaranteed high returns
- Romance scams involving requests for money

**Response Guidelines:**
- For HIGH/CRITICAL threats: Immediately warn user, provide emergency contacts, and advise stopping all communication
- For MEDIUM threats: Explain concerns clearly and provide protective measures
- For LOW threats: Offer guidance while encouraging continued vigilance
- Always provide specific next steps and resources
- Include relevant contact information for reporting scams
- Encourage users to verify information through official channels

**Important Reminders:**
- Never provide personal financial advice beyond general security guidance
- Always encourage users to contact official organizations directly
- Emphasize that legitimate organizations never ask for sensitive information via email/phone
- Remind users that if something seems too good to be true, it probably is
- Encourage users to trust their instincts when something feels wrong

Your responses should be clear, actionable, and focused on immediate user protection while building long-term security awareness."""

    async def generate_fraud_advice(
        self,
        user_message: str,
        session_context: Dict[str, Any],
        risk_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate fraud advice using Hugging Face GPT-OSS model

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
                    "content": "AI service is currently unavailable. Please contact a human advisor immediately if you believe you're being targeted by a scam.",
                    "confidence": 0.0,
                    "model": "unavailable",
                }

            # Prepare the conversation context
            messages = [
                {"role": "system", "content": self._get_cybersecurity_system_prompt()},
                {
                    "role": "user",
                    "content": f"""Context: Risk Level: {risk_analysis.get("risk_level", "unknown")}, Fraud Type: {risk_analysis.get("fraud_type", "unknown")}

User Message: {user_message}

Please analyze this situation and provide specific cybersecurity guidance. Focus on immediate protection measures and warning signs to watch for.""",
                },
            ]

            # Make API call to Hugging Face Inference
            response = self.client.chat.completion(
                model="microsoft/DialoGPT-large",  # Using a more capable model
                messages=messages,
                max_tokens=500,
                temperature=0.7,
                top_p=0.9,
            )

            # Extract response content
            if response and "choices" in response and len(response["choices"]) > 0:
                content = response["choices"][0]["message"]["content"]

                # Calculate confidence based on risk level and response quality
                confidence = self._calculate_confidence(risk_analysis, content)

                return {
                    "content": content,
                    "confidence": confidence,
                    "model": "huggingface-gpt-oss",
                    "reasoning": f"AI analysis based on {risk_analysis.get('risk_level', 'unknown')} risk level and fraud type: {risk_analysis.get('fraud_type', 'unknown')}",
                }
            else:
                logger.error("Invalid response format from Hugging Face API")
                return self._generate_fallback_response(user_message, risk_analysis)

        except Exception as e:
            logger.error(f"Error generating Hugging Face response: {str(e)}")
            return {
                "content": "I'm experiencing technical difficulties. Please try again or contact a human advisor immediately if you believe you're being targeted by a scam.",
                "confidence": 0.0,
                "model": "error",
            }

    def _calculate_confidence(
        self, risk_analysis: Dict[str, Any], content: str
    ) -> float:
        """
        Calculate confidence score based on risk analysis and response quality
        """
        base_confidence = 0.8

        # Adjust based on risk level
        risk_level = risk_analysis.get("risk_level", "low")
        if risk_level == "critical":
            base_confidence += 0.15
        elif risk_level == "high":
            base_confidence += 0.1
        elif risk_level == "medium":
            base_confidence += 0.05

        # Adjust based on response quality indicators
        if any(
            keyword in content.lower()
            for keyword in ["immediately", "urgent", "stop", "danger"]
        ):
            base_confidence += 0.05

        if any(
            keyword in content.lower()
            for keyword in ["contact", "report", "verify", "check"]
        ):
            base_confidence += 0.05

        return min(base_confidence, 1.0)

    def _generate_fallback_response(
        self, user_message: str, risk_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate a fallback response when API is unavailable

        Args:
            user_message: User's message
            risk_analysis: Risk analysis results

        Returns:
            Fallback response
        """
        fraud_type = risk_analysis.get("fraud_type", "unknown")
        risk_level = risk_analysis.get("risk_level", "low")

        if risk_level == "critical":
            content = f"""🚨 CRITICAL SECURITY ALERT 🚨

This {fraud_type} situation is extremely dangerous and requires immediate action:

1. STOP all communication immediately
2. Do NOT send any money or personal information
3. Contact your bank/financial institution immediately
4. Report to Action Fraud (UK) or your local fraud reporting agency
5. Change all passwords if you've shared any personal information

This appears to be a sophisticated scam targeting you for financial gain."""

        elif risk_level == "high":
            content = f"""⚠️ HIGH RISK WARNING ⚠️

I'm very concerned about this {fraud_type} situation. Multiple red flags suggest this is a scam:

1. Cease all communication immediately
2. Do NOT provide any personal or financial information
3. Verify any claims through official channels
4. Be extremely cautious of any requests for money
5. Trust your instincts - if it feels wrong, it probably is

Legitimate organizations never pressure you for immediate action or payment."""

        elif risk_level == "medium":
            content = f"""⚠️ CAUTION ADVISED ⚠️

This {fraud_type} situation has concerning elements that warrant careful evaluation:

1. Verify all claims through official sources
2. Never share personal or financial information
3. Be suspicious of unsolicited contact
4. Look for official communication channels
5. Take your time to research before any action

When in doubt, contact the organization directly through their official website or phone number."""

        else:
            content = f"""✅ GENERAL SECURITY GUIDANCE ✅

While this {fraud_type} situation may not pose an immediate threat, it's excellent that you're being cautious:

1. Always verify information through official channels
2. Be suspicious of unsolicited contact
3. Never share personal information unless you initiated contact
4. Trust your instincts
5. When in doubt, ask for help

Remember: Legitimate organizations respect your need to verify information."""

        return {
            "content": content,
            "confidence": 0.6,
            "model": "fallback",
            "reasoning": "Fallback response due to API unavailability",
        }

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

            # Use AI for enhanced analysis
            analysis_prompt = f"""Analyze this message for fraud indicators:

Message: "{message}"
Known fraud type: {fraud_type or "unknown"}
User vulnerability factors: {vulnerability_factors or "none"}

Provide analysis focusing on:
1. Fraud type classification
2. Risk level assessment (low/medium/high/critical)
3. Key warning signs detected
4. Confidence level

Respond in JSON format with fraud_type, risk_level, confidence, and warning_signs."""

            messages = [
                {
                    "role": "system",
                    "content": "You are a cybersecurity expert specializing in fraud detection. Analyze messages for scam indicators and provide structured risk assessments.",
                },
                {"role": "user", "content": analysis_prompt},
            ]

            response = self.client.chat.completion(
                model="microsoft/DialoGPT-large",
                messages=messages,
                max_tokens=300,
                temperature=0.3,
            )

            if response and "choices" in response and len(response["choices"]) > 0:
                content = response["choices"][0]["message"]["content"]

                # Parse AI response (fallback to basic analysis if parsing fails)
                try:
                    import json

                    ai_analysis = json.loads(content)
                    return {
                        "fraud_type": ai_analysis.get(
                            "fraud_type", fraud_type or "unknown"
                        ),
                        "risk_level": ai_analysis.get("risk_level", "medium"),
                        "confidence": ai_analysis.get("confidence", 0.7),
                        "ai_available": True,
                        "warning_signs": ai_analysis.get("warning_signs", []),
                    }
                except:
                    # Fallback to basic analysis if JSON parsing fails
                    return self._basic_ai_analysis(
                        message, fraud_type, vulnerability_factors
                    )
            else:
                return self._basic_ai_analysis(
                    message, fraud_type, vulnerability_factors
                )

        except Exception as e:
            logger.error(f"Error in AI message analysis: {str(e)}")
            return self._basic_ai_analysis(message, fraud_type, vulnerability_factors)

    def _basic_ai_analysis(
        self,
        message: str,
        fraud_type: Optional[str] = None,
        vulnerability_factors: Optional[list] = None,
    ) -> Dict[str, Any]:
        """
        Enhanced basic analysis using keyword matching and rules
        """
        message_lower = message.lower()

        # Detect fraud type if not provided
        if not fraud_type:
            if any(
                word in message_lower
                for word in ["phish", "email", "link", "click", "verify", "account"]
            ):
                fraud_type = "phishing"
            elif any(
                word in message_lower
                for word in [
                    "love",
                    "romance",
                    "relationship",
                    "marriage",
                    "boyfriend",
                    "girlfriend",
                ]
            ):
                fraud_type = "romance_scam"
            elif any(
                word in message_lower
                for word in [
                    "invest",
                    "money",
                    "profit",
                    "crypto",
                    "bitcoin",
                    "trading",
                ]
            ):
                fraud_type = "investment_scam"
            elif any(
                word in message_lower
                for word in ["support", "computer", "virus", "malware", "fix"]
            ):
                fraud_type = "tech_support"
            else:
                fraud_type = "unknown"

        # Assess risk level with enhanced detection
        risk_level = "low"
        confidence = 0.6
        warning_signs = []

        # Critical risk indicators
        critical_words = [
            "bank transfer",
            "gift cards",
            "bitcoin",
            "crypto",
            "wire transfer",
            "western union",
        ]
        if any(word in message_lower for word in critical_words):
            risk_level = "critical"
            confidence += 0.3
            warning_signs.extend(
                [word for word in critical_words if word in message_lower]
            )

        # High-risk indicators
        high_risk_words = [
            "urgent",
            "immediate",
            "now",
            "limited time",
            "act fast",
            "expires soon",
        ]
        if any(word in message_lower for word in high_risk_words):
            if risk_level != "critical":
                risk_level = "high"
            confidence += 0.2
            warning_signs.extend(
                [word for word in high_risk_words if word in message_lower]
            )

        # Medium risk indicators
        medium_risk_words = [
            "free",
            "winner",
            "congratulations",
            "claim",
            "verify",
            "suspended",
        ]
        if any(word in message_lower for word in medium_risk_words):
            if risk_level == "low":
                risk_level = "medium"
            confidence += 0.1
            warning_signs.extend(
                [word for word in medium_risk_words if word in message_lower]
            )

        # Adjust based on vulnerability factors
        if vulnerability_factors:
            if "elderly" in vulnerability_factors:
                if risk_level == "low":
                    risk_level = "medium"
                elif risk_level == "medium":
                    risk_level = "high"
                confidence += 0.1
                warning_signs.append("elderly_vulnerability")

        return {
            "fraud_type": fraud_type,
            "risk_level": risk_level,
            "confidence": min(confidence, 1.0),
            "warning_signs": warning_signs,
            "ai_available": False,
        }
