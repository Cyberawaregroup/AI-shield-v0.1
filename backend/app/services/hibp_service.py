import httpx
import logging
from typing import List, Optional, Dict, Any
from app.core.config import settings
import time

logger = logging.getLogger(__name__)

class HIBPService:
    def __init__(self):
        self.api_key = settings.HIBP_API_KEY
        self.base_url = "https://haveibeenpwned.com/api/v3"
        self.rate_limit_delay = 1.6  # HIBP requires 1.6 seconds between requests
        
    async def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Make a request to HIBP API with proper headers and rate limiting"""
        if not self.api_key:
            logger.warning("HIBP API key not configured. Using mock data.")
            return None
            
        headers = {
            "hibp-api-key": self.api_key,
            "user-agent": "AI-Shield-Sentinel/1.0"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}{endpoint}",
                    headers=headers,
                    params=params,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    # No breaches found
                    return []
                elif response.status_code == 429:
                    logger.warning("HIBP rate limit exceeded. Waiting before retry.")
                    time.sleep(self.rate_limit_delay)
                    return None
                else:
                    logger.error(f"HIBP API error: {response.status_code} - {response.text}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error making HIBP request: {e}")
            return None

    async def check_email(self, email: str) -> List[Dict[str, Any]]:
        """Check if an email has been involved in data breaches"""
        if not self.api_key:
            # Return mock data for testing
            return self._get_mock_breaches(email)
            
        endpoint = f"/breachedaccount/{email}"
        result = await self._make_request(endpoint)
        
        if result is None:
            return []
            
        # Add delay for rate limiting
        time.sleep(self.rate_limit_delay)
        return result

    async def check_domain(self, domain: str) -> List[Dict[str, Any]]:
        """Check if a domain has been involved in data breaches"""
        if not self.api_key:
            # Return mock data for testing
            return self._get_mock_domain_breaches(domain)
            
        endpoint = f"/breaches?domain={domain}"
        result = await self._make_request(endpoint)
        
        if result is None:
            return []
            
        # Add delay for rate limiting
        time.sleep(self.rate_limit_delay)
        return result

    async def get_breach_details(self, breach_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific breach"""
        if not self.api_key:
            # Return mock data for testing
            return self._get_mock_breach_details(breach_name)
            
        endpoint = f"/breach/{breach_name}"
        result = await self._make_request(endpoint)
        
        if result is None:
            return None
            
        # Add delay for rate limiting
        time.sleep(self.rate_limit_delay)
        return result

    async def check_password(self, password: str) -> bool:
        """Check if a password has been compromised (using SHA1 hash)"""
        if not self.api_key:
            # Return mock data for testing
            return self._get_mock_password_check(password)
            
        import hashlib
        password_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix = password_hash[:5]
        suffix = password_hash[5:]
        
        endpoint = f"/range/{prefix}"
        result = await self._make_request(endpoint)
        
        if result is None:
            return False
            
        # Check if the suffix exists in the response
        lines = result.split('\n')
        for line in lines:
            if line.startswith(suffix):
                count = int(line.split(':')[1])
                return count > 0
                
        # Add delay for rate limiting
        time.sleep(self.rate_limit_delay)
        return False

    def _get_mock_breaches(self, email: str) -> List[Dict[str, Any]]:
        """Return mock breach data for testing when API key is not available"""
        return [
            {
                "Name": "Adobe Data Breach 2013",
                "Title": "Adobe",
                "Domain": "adobe.com",
                "BreachDate": "2013-10-03",
                "AddedDate": "2013-12-04T00:00:00Z",
                "ModifiedDate": "2013-12-04T00:00:00Z",
                "PwnCount": 152445165,
                "Description": "In October 2013, 153 million Adobe accounts were breached with each containing an internal ID, username, email, encrypted password and a password hint in plain text.",
                "DataClasses": ["Email addresses", "Password hints", "Passwords", "Usernames"],
                "IsVerified": True,
                "IsFabricated": False,
                "IsSensitive": False,
                "IsRetired": False,
                "IsSpamList": False,
                "LogoPath": "https://haveibeenpwned.com/Content/Images/PwnedLogos/Adobe.png"
            },
            {
                "Name": "LinkedIn Data Breach 2012",
                "Title": "LinkedIn",
                "Domain": "linkedin.com",
                "BreachDate": "2012-05-05",
                "AddedDate": "2016-05-21T21:35:40Z",
                "ModifiedDate": "2016-05-21T21:35:40Z",
                "PwnCount": 164611595,
                "Description": "In May 2016, LinkedIn had 164 million email addresses and passwords exposed. Originally hacked in 2012, the data remained out of sight until being offered for sale on a dark market site 4 years later.",
                "DataClasses": ["Email addresses", "Passwords"],
                "IsVerified": True,
                "IsFabricated": False,
                "IsSensitive": False,
                "IsRetired": False,
                "IsSpamList": False,
                "LogoPath": "https://haveibeenpwned.com/Content/Images/PwnedLogos/LinkedIn.png"
            }
        ]

    def _get_mock_domain_breaches(self, domain: str) -> List[Dict[str, Any]]:
        """Return mock domain breach data for testing"""
        return [
            {
                "Name": f"Mock Breach for {domain}",
                "Title": domain,
                "Domain": domain,
                "BreachDate": "2023-01-01",
                "PwnCount": 1000,
                "Description": f"Mock data breach for {domain}",
                "DataClasses": ["Email addresses", "Passwords"]
            }
        ]

    def _get_mock_breach_details(self, breach_name: str) -> Dict[str, Any]:
        """Return mock breach details for testing"""
        return {
            "Name": breach_name,
            "Title": breach_name,
            "Domain": "example.com",
            "BreachDate": "2023-01-01",
            "PwnCount": 1000,
            "Description": f"Mock breach details for {breach_name}",
            "DataClasses": ["Email addresses", "Passwords"]
        }

    def _get_mock_password_check(self, password: str) -> bool:
        """Return mock password check result for testing"""
        # Mock: consider passwords with 'password' or '123' as compromised
        return 'password' in password.lower() or '123' in password
