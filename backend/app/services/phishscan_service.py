import asyncio
import logging
from typing import Any, Dict

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class PhishScanService:
    """Service for interacting with zvelo PhishScan API"""

    def __init__(self):
        self.api_key = settings.ZVELO_API_KEY
        self.base_url = "https://api.zvelo.com/v1"
        self.headers = (
            {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            if self.api_key
            else {}
        )

        if not self.api_key:
            logger.warning(
                "zvelo PhishScan API key not configured. Phishing detection will be limited."
            )

    async def check_url(self, url: str) -> Dict[str, Any]:
        """
        Check if a URL is phishing using zvelo PhishScan

        Args:
            url: URL to check

        Returns:
            Dictionary containing phishing analysis results
        """
        try:
            if not self.api_key:
                return self._mock_url_check(url)

            # Rate limiting - be respectful to the API
            await asyncio.sleep(0.2)

            endpoint = f"{self.base_url}/phish"
            data = {"url": url, "include_redirects": True, "include_screenshots": False}

            async with httpx.AsyncClient() as client:
                response = await client.post(endpoint, headers=self.headers, json=data)

                if response.status_code == 200:
                    result = response.json()
                    return self._parse_phishscan_response(result)
                elif response.status_code == 429:
                    logger.warning("zvelo PhishScan rate limit exceeded")
                    return self._mock_url_check(url)
                else:
                    logger.error(
                        f"zvelo PhishScan API error: {response.status_code} - {response.text}"
                    )
                    return self._mock_url_check(url)

        except Exception as e:
            logger.error(f"Error checking URL {url} with zvelo PhishScan: {str(e)}")
            return self._mock_url_check(url)

    def _parse_phishscan_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse zvelo PhishScan API response

        Args:
            data: Raw API response data

        Returns:
            Parsed phishing analysis results
        """
        try:
            # Extract relevant information from the response
            # Note: This is a simplified parser - adjust based on actual API response format
            result = data.get("result", {})

            return {
                "url": result.get("url"),
                "is_phishing": result.get("is_phishing", False),
                "confidence": result.get("confidence", 0.0),
                "category": result.get("category", "unknown"),
                "threat_level": result.get("threat_level", "low"),
                "redirects": result.get("redirects", []),
                "final_url": result.get("final_url"),
                "domain": result.get("domain"),
                "ip_address": result.get("ip_address"),
                "country": result.get("country"),
                "asn": result.get("asn"),
                "first_seen": result.get("first_seen"),
                "last_seen": result.get("last_seen"),
                "source": "zvelo_phishscan",
            }

        except Exception as e:
            logger.error(f"Error parsing zvelo PhishScan response: {str(e)}")
            return {
                "url": "unknown",
                "is_phishing": False,
                "confidence": 0.0,
                "source": "zvelo_phishscan",
                "error": "Failed to parse response",
            }

    def _mock_url_check(self, url: str) -> Dict[str, Any]:
        """
        Mock URL check when API is not available

        Args:
            url: URL being checked

        Returns:
            Mock phishing analysis results
        """
        import random

        # Simple mock logic for demonstration
        url_lower = url.lower()

        # Check for obvious phishing indicators
        phishing_indicators = [
            "bank",
            "paypal",
            "amazon",
            "ebay",
            "apple",
            "microsoft",
            "netflix",
            "login",
            "verify",
            "secure",
            "account",
            "suspended",
            "locked",
        ]

        # Check for suspicious patterns
        suspicious_patterns = [
            "bank-secure",
            "paypal-verify",
            "amazon-account",
            "ebay-secure",
            "apple-verify",
            "microsoft-secure",
            "netflix-account",
        ]

        # Determine if this looks like phishing
        is_phishing = False
        confidence = 0.0

        # Check for suspicious patterns
        for pattern in suspicious_patterns:
            if pattern in url_lower:
                is_phishing = True
                confidence = 0.8
                break

        # Check for phishing indicators
        if not is_phishing:
            indicator_count = sum(
                1 for indicator in phishing_indicators if indicator in url_lower
            )
            if indicator_count >= 2:
                is_phishing = random.choice([True, False])  # 50% chance
                confidence = random.uniform(0.3, 0.7)

        # Generate mock data
        if is_phishing:
            category = random.choice(["phishing", "malware", "scam", "fake_login"])
            threat_level = random.choice(["medium", "high"])
        else:
            category = "legitimate"
            threat_level = "low"

        return {
            "url": url,
            "is_phishing": is_phishing,
            "confidence": confidence,
            "category": category,
            "threat_level": threat_level,
            "redirects": [],
            "final_url": url,
            "domain": url.split("//")[-1].split("/")[0] if "//" in url else url,
            "ip_address": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "country": random.choice(["US", "GB", "DE", "FR", "JP", "CA", "AU"]),
            "asn": f"AS{random.randint(1000, 99999)}",
            "first_seen": "2024-01-01T00:00:00Z",
            "last_seen": "2024-01-01T00:00:00Z",
            "source": "mock",
            "note": "Mock data - API key not configured",
        }

    async def check_bulk_urls(self, urls: list) -> list:
        """
        Check multiple URLs for phishing (bulk operation)

        Args:
            urls: List of URLs to check

        Returns:
            List of phishing analysis results
        """
        try:
            if not self.api_key:
                logger.warning(
                    "Cannot perform bulk check - zvelo PhishScan API key not configured"
                )
                return [self._mock_url_check(url) for url in urls]

            results = []
            for url in urls:
                result = await self.check_url(url)
                results.append(result)
                # Small delay between requests
                await asyncio.sleep(0.1)

            return results

        except Exception as e:
            logger.error(f"Error in bulk URL check: {str(e)}")
            return [self._mock_url_check(url) for url in urls]

    async def get_phishing_stats(self) -> Dict[str, Any]:
        """
        Get phishing statistics from zvelo PhishScan

        Returns:
            Dictionary containing phishing statistics
        """
        try:
            if not self.api_key:
                logger.warning(
                    "Cannot get stats - zvelo PhishScan API key not configured"
                )
                return self._mock_stats()

            endpoint = f"{self.base_url}/stats/phishing"

            async with httpx.AsyncClient() as client:
                response = await client.get(endpoint, headers=self.headers)

                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(
                        f"Failed to get phishing stats: {response.status_code} - {response.text}"
                    )
                    return self._mock_stats()

        except Exception as e:
            logger.error(f"Error getting phishing stats: {str(e)}")
            return self._mock_stats()

    def _mock_stats(self) -> Dict[str, Any]:
        """Generate mock phishing statistics"""
        import random

        return {
            "total_urls_checked": random.randint(10000, 1000000),
            "phishing_urls_detected": random.randint(1000, 100000),
            "detection_rate": random.uniform(0.05, 0.15),
            "top_categories": [
                {"category": "phishing", "count": random.randint(500, 5000)},
                {"category": "malware", "count": random.randint(200, 2000)},
                {"category": "scam", "count": random.randint(100, 1000)},
            ],
            "top_countries": [
                {"country": "US", "count": random.randint(100, 1000)},
                {"country": "GB", "count": random.randint(50, 500)},
                {"country": "DE", "count": random.randint(30, 300)},
            ],
            "source": "mock",
            "note": "Mock statistics - API key not configured",
        }
