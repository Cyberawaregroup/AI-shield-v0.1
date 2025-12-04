import hashlib
import logging
from typing import Any, Dict, List, Optional

from app.clients.hibp import (
    HIBPAsyncClient,
    HIBPAuthError,
    HIBPError,
    HIBPRateLimitError,
)
from app.core.config import settings
from app.services.base import Service, ServiceError

logger = logging.getLogger(__name__)


class HIBPService(Service):
    """Service for interacting with Have I Been Pwned API"""

    id = "hibp"
    name = "Have I Been Pwned"

    def __init__(
        self,
        client: Optional[HIBPAsyncClient] = None,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize HIBP service.

        :param client: Optional HIBPAsyncClient instance. If not provided, will create one
            if API key is available, otherwise will use mock mode.
        :param logger: Optional logger instance
        """
        super().__init__(logger=logger)
        self.client = client

        if self.client is None and settings.HIBP_API_KEY:
            self.client = HIBPAsyncClient(api_key=settings.HIBP_API_KEY)
            if self.logger:
                self.logger.info("Initialized HIBPService with HIBP API client")
        elif self.client is None:
            if self.logger:
                self.logger.warning(
                    "HIBP API key not configured. Service will operate in mock mode."
                )

    def _is_mock_mode(self) -> bool:
        """Check if service is running in mock mode."""
        return self.client is None

    def _mock_breaches(self, email: str) -> List[Dict[str, Any]]:
        """Return mock breach data for testing."""
        return [
            {
                "Name": "MockBreach2023",
                "Title": "Mock Data Breach 2023",
                "Domain": "mocksite.com",
                "BreachDate": "2023-01-15",
                "AddedDate": "2023-02-01T00:00:00Z",
                "ModifiedDate": "2023-02-01T00:00:00Z",
                "PwnCount": 10000,
                "Description": "This is a mock breach for testing purposes.",
                "DataClasses": ["Email addresses", "Passwords", "Usernames"],
                "IsVerified": True,
                "IsFabricated": False,
                "IsSensitive": False,
                "IsRetired": False,
                "IsSpamList": False,
                "IsMalware": False,
                "IsSubscriptionFree": True,
                "LogoPath": "https://haveibeenpwned.com/Content/Images/PwnedLogos/MockBreach.png",
            }
        ]

    def _mock_pastes(self, email: str) -> List[Dict[str, Any]]:
        """Return mock paste data for testing."""
        return [
            {
                "Source": "Pastebin",
                "Id": "mock123",
                "Title": "Mock Paste",
                "Date": "2023-03-15T10:30:00Z",
                "EmailCount": 5,
            }
        ]

    def _mock_all_breaches(self) -> List[Dict[str, Any]]:
        """Return mock list of all breaches."""
        return [
            {
                "Name": "Adobe",
                "Title": "Adobe",
                "Domain": "adobe.com",
                "BreachDate": "2013-10-04",
                "AddedDate": "2013-12-04T00:00:00Z",
                "ModifiedDate": "2022-05-15T23:52:49Z",
                "PwnCount": 152445165,
                "Description": "Mock Adobe breach data",
                "DataClasses": [
                    "Email addresses",
                    "Password hints",
                    "Passwords",
                    "Usernames",
                ],
                "IsVerified": True,
                "IsFabricated": False,
                "IsSensitive": False,
                "IsRetired": False,
                "IsSpamList": False,
                "IsMalware": False,
                "IsSubscriptionFree": True,
                "LogoPath": "https://haveibeenpwned.com/Content/Images/PwnedLogos/Adobe.png",
            }
        ]

    def _mock_data_classes(self) -> List[str]:
        """Return mock list of data classes."""
        return [
            "Account balances",
            "Age groups",
            "Ages",
            "Apps installed on devices",
            "Audio recordings",
            "Auth tokens",
            "Avatars",
            "Bank account numbers",
            "Banking PINs",
            "Beauty ratings",
            "Biometric data",
            "Browser user agent details",
            "Buying preferences",
            "Car ownership statuses",
            "Career levels",
            "Cellular network names",
            "Charitable donations",
            "Chat logs",
            "Credit card CVV",
            "Credit cards",
            "Credit status information",
            "Customer feedback",
            "Customer interactions",
            "Dates of birth",
            "Deceased date",
            "Device information",
            "Device usage tracking data",
            "Drinking habits",
            "Drug habits",
            "Eating habits",
            "Education levels",
            "Email addresses",
            "Email messages",
            "Employers",
            "Ethnicities",
            "Family members' names",
            "Family plans",
            "Family structure",
            "Financial investments",
            "Financial transactions",
            "Fitness levels",
            "Genders",
            "Geographic locations",
            "Government issued IDs",
            "Historical passwords",
            "Home loan information",
            "Home ownership statuses",
            "Homepage URLs",
            "IMEI numbers",
            "IMSI numbers",
            "Income levels",
            "Instant messenger identities",
            "IP addresses",
            "Job titles",
            "MAC addresses",
            "Marital statuses",
            "Names",
            "Nationalities",
            "Net worths",
            "Nicknames",
            "Parenting plans",
            "Partial credit card data",
            "Passport numbers",
            "Password hints",
            "Passwords",
            "Payment histories",
            "Payment methods",
            "Personal descriptions",
            "Personal health data",
            "Personal interests",
            "Phone numbers",
            "Photos",
            "Physical addresses",
            "Physical attributes",
            "PINs",
            "Places of birth",
            "Political donations",
            "Political views",
            "Private messages",
            "Professional skills",
            "Profile photos",
            "Purchases",
            "Purchasing habits",
            "Races",
            "Recovery email addresses",
            "Relationship statuses",
            "Religions",
            "Reward program balances",
            "Salaries",
            "School grades (class levels)",
            "Security questions and answers",
            "Sexual fetishes",
            "Sexual orientations",
            "Smoking habits",
            "SMS messages",
            "Social connections",
            "Social media profiles",
            "Spoken languages",
            "Support tickets",
            "Survey results",
            "Time zones",
            "Travel habits",
            "User statuses",
            "User website URLs",
            "Usernames",
            "Utility bill payments",
            "Vehicle details",
            "Website activity",
            "Work habits",
            "Years of birth",
            "Years of professional experience",
        ]

    async def check_email(
        self,
        email: str,
        truncate_response: bool = False,
        include_unverified: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        Check if an email address has been involved in data breaches.

        :param email: Email address to check
        :param truncate_response: Return only breach names (faster)
        :param include_unverified: Include unverified breaches
        :return: List of breach dictionaries or list of breach names if truncated
        """
        try:
            if self._is_mock_mode():
                if self.logger:
                    self.logger.info(f"Mock mode: Checking email {email}")
                return self._mock_breaches(email)

            assert self.client is not None, "Client should not be None in non-mock mode"

            breaches = await self.client.get_account_breaches(
                account=email,
                truncate_response=truncate_response,
                include_unverified=include_unverified,
            )

            if breaches is None:
                if self.logger:
                    self.logger.info(f"No breaches found for email: {email}")
                return []

            return [breach.model_dump() for breach in breaches]

        except HIBPRateLimitError as e:
            if self.logger:
                self.logger.warning(f"Rate limit hit checking email {email}: {e}")
            raise ServiceError(
                f"Rate limit exceeded for HIBP API: {str(e)}",
                self.name,
                http_status=429,
            ) from e
        except HIBPAuthError as e:
            if self.logger:
                self.logger.error(f"Authentication error checking email {email}: {e}")
            raise ServiceError(
                f"Authentication failed for HIBP API: {str(e)}",
                self.name,
                http_status=401,
            ) from e
        except HIBPError as e:
            if self.logger:
                self.logger.error(f"{type(e).__name__} checking email {email}: {e}")
            raise ServiceError(
                f"HIBP API error checking email: {str(e)}",
                self.name,
                http_status=500,
            ) from e
        except Exception as e:
            if self.logger:
                self.logger.error(f"Unexpected error checking email {email}: {e}")
            raise ServiceError(
                f"Unexpected error checking email: {str(e)}",
                self.name,
                http_status=500,
            ) from e

    async def check_domain(self, domain: str) -> List[Dict[str, Any]]:
        """
        Check if a domain has been involved in data breaches.

        :param domain: Domain name to check
        :return: List of breach dictionaries
        """
        try:
            if self._is_mock_mode():
                if self.logger:
                    self.logger.info(f"Mock mode: Checking domain {domain}")
                return self._mock_all_breaches()

            assert self.client is not None, "Client should not be None in non-mock mode"
            breaches = await self.client.get_all_breaches(domain=domain)

            if breaches is None:
                return []
            return [breach.model_dump() for breach in breaches]

        except HIBPError as e:
            if self.logger:
                self.logger.error(f"{type(e).__name__} checking domain {domain}: {e}")
            raise ServiceError(
                f"HIBP API error checking domain: {str(e)}",
                self.name,
                http_status=500,
            ) from e
        except Exception as e:
            if self.logger:
                self.logger.error(f"Unexpected error checking domain {domain}: {e}")
            raise ServiceError(
                f"Unexpected error checking domain: {str(e)}",
                self.name,
                http_status=500,
            ) from e

    async def get_breach_details(self, breach_name: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific breach.

        :param breach_name: Name of the breach
        :return: Breach dictionary or None if not found
        """
        try:
            if self._is_mock_mode():
                if self.logger:
                    self.logger.info(f"Mock mode: Getting breach {breach_name}")
                mock_breaches = self._mock_all_breaches()
                for breach in mock_breaches:
                    if breach["Name"].lower() == breach_name.lower():
                        return breach
                return None

            assert self.client is not None, "Client should not be None in non-mock mode"
            breach = await self.client.get_breach(name=breach_name)
            if breach is None:
                return None
            return breach.model_dump()

        except HIBPError as e:
            if self.logger:
                self.logger.error(
                    f"{type(e).__name__} getting breach {breach_name}: {e}"
                )
            raise ServiceError(
                f"HIBP API error getting breach details: {str(e)}",
                self.name,
                http_status=500,
            ) from e
        except Exception as e:
            if self.logger:
                self.logger.error(f"Unexpected error getting breach {breach_name}: {e}")
            raise ServiceError(
                f"Unexpected error getting breach details: {str(e)}",
                self.name,
                http_status=500,
            ) from e

    async def check_password(self, password: str) -> bool:
        """
        Check if a password has been compromised using the Pwned Passwords API.

        :param password: Password to check
        :return: True if password has been compromised, False otherwise
        """
        try:
            if self._is_mock_mode():
                if self.logger:
                    self.logger.info("Mock mode: Checking password")
                return self._mock_password_check(password)

            assert self.client is not None, "Client should not be None in non-mock mode"
            # Hash the password with SHA-1
            password_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
            result = await self.client.check_password_pwned(
                password_hash=password_hash, hash_mode="sha1"
            )
            return bool(result)

        except HIBPError as e:
            if self.logger:
                self.logger.error(f"{type(e).__name__} checking password: {e}")
            raise ServiceError(
                f"HIBP API error checking password: {str(e)}",
                self.name,
                http_status=500,
            ) from e
        except Exception as e:
            if self.logger:
                self.logger.error(f"Unexpected error checking password: {e}")
            raise ServiceError(
                f"Unexpected error checking password: {str(e)}",
                self.name,
                http_status=500,
            ) from e

    def _mock_password_check(self, password: str) -> bool:
        """Return mock password check result for testing."""
        # Mock: consider passwords with 'password' or '123' as compromised
        return "password" in password.lower() or "123" in password
