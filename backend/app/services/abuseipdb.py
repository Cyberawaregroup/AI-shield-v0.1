import asyncio
import logging
from typing import Any, Dict

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class AbuseIPDBService:
    """Service for interacting with AbuseIPDB API"""

    def __init__(self):
        self.api_key = settings.ABUSEIPDB_API_KEY
        self.base_url = "https://api.abuseipdb.com/api/v2"
        self.headers = (
            {"Accept": "application/json", "Key": self.api_key} if self.api_key else {}
        )

        if not self.api_key:
            logger.warning(
                "AbuseIPDB API key not configured. IP reputation checking will be limited."
            )

    async def check_ip(self, ip_address: str) -> Dict[str, Any]:
        """
        Check IP address reputation using AbuseIPDB

        Args:
            ip_address: IP address to check

        Returns:
            Dictionary containing reputation information
        """
        try:
            if not self.api_key:
                return self._mock_ip_check(ip_address)

            # Rate limiting - AbuseIPDB allows 1000 requests per day
            await asyncio.sleep(0.1)  # Small delay to be respectful

            url = f"{self.base_url}/check"
            params = {
                "ipAddress": ip_address,
                "maxAgeInDays": "90",  # Check last 90 days
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers, params=params)

                if response.status_code == 200:
                    data = response.json()
                    return self._parse_abuseipdb_response(data)
                elif response.status_code == 429:
                    logger.warning("AbuseIPDB rate limit exceeded")
                    return self._mock_ip_check(ip_address)
                else:
                    logger.error(
                        f"AbuseIPDB API error: {response.status_code} - {response.text}"
                    )
                    return self._mock_ip_check(ip_address)

        except Exception as e:
            logger.error(f"Error checking IP {ip_address} with AbuseIPDB: {str(e)}")
            return self._mock_ip_check(ip_address)

    def _parse_abuseipdb_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse AbuseIPDB API response

        Args:
            data: Raw API response data

        Returns:
            Parsed reputation information
        """
        try:
            data_obj = data.get("data", {})

            return {
                "ip_address": data_obj.get("ipAddress"),
                "is_public": data_obj.get("isPublic", True),
                "ip_version": data_obj.get("ipVersion", 4),
                "is_whitelisted": data_obj.get("isWhitelisted", False),
                "abuse_confidence_score": data_obj.get("abuseConfidenceScore", 0),
                "country_code": data_obj.get("countryCode"),
                "usage_type": data_obj.get("usageType"),
                "isp": data_obj.get("isp"),
                "domain": data_obj.get("domain"),
                "hostnames": data_obj.get("hostnames", []),
                "total_reports": data_obj.get("totalReports", 0),
                "num_distinct_users": data_obj.get("numDistinctUsers", 0),
                "last_reported_at": data_obj.get("lastReportedAt"),
                "reports": data_obj.get("reports", []),
                "source": "abuseipdb",
            }

        except Exception as e:
            logger.error(f"Error parsing AbuseIPDB response: {str(e)}")
            return {
                "ip_address": "unknown",
                "abuse_confidence_score": 0,
                "total_reports": 0,
                "source": "abuseipdb",
                "error": "Failed to parse response",
            }

    def _mock_ip_check(self, ip_address: str) -> Dict[str, Any]:
        """
        Mock IP check when API is not available

        Args:
            ip_address: IP address being checked

        Returns:
            Mock reputation information
        """
        # Simple mock logic for demonstration
        if (
            ip_address.startswith("192.168.")
            or ip_address.startswith("10.")
            or ip_address.startswith("172.")
        ):
            # Private IP addresses
            return {
                "ip_address": ip_address,
                "is_public": False,
                "abuse_confidence_score": 0,
                "total_reports": 0,
                "source": "mock",
                "note": "Private IP address - no reputation data available",
            }
        elif ip_address in ["8.8.8.8", "1.1.1.1"]:
            # Known good IPs
            return {
                "ip_address": ip_address,
                "is_public": True,
                "abuse_confidence_score": 0,
                "total_reports": 0,
                "source": "mock",
                "note": "Known good IP address",
            }
        else:
            # Random mock data for demonstration
            import random

            abuse_score = random.randint(0, 100)

            return {
                "ip_address": ip_address,
                "is_public": True,
                "abuse_confidence_score": abuse_score,
                "total_reports": random.randint(0, 50) if abuse_score > 20 else 0,
                "country_code": random.choice(["US", "GB", "DE", "FR", "JP"]),
                "usage_type": random.choice(
                    ["ISP", "Hosting", "Residential", "Mobile"]
                ),
                "source": "mock",
                "note": "Mock data - API key not configured",
            }

    async def report_ip(
        self, ip_address: str, categories: list, comment: str = ""
    ) -> bool:
        """
        Report an IP address to AbuseIPDB

        Args:
            ip_address: IP address to report
            categories: List of abuse categories
            comment: Additional comment about the abuse

        Returns:
            True if report successful, False otherwise
        """
        try:
            if not self.api_key:
                logger.warning("Cannot report IP - AbuseIPDB API key not configured")
                return False

            url = f"{self.base_url}/report"
            data = {
                "ip": ip_address,
                "categories": ",".join(map(str, categories)),
                "comment": comment,
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=self.headers, data=data)

                if response.status_code == 200:
                    logger.info(f"Successfully reported IP {ip_address} to AbuseIPDB")
                    return True
                else:
                    logger.error(
                        f"Failed to report IP {ip_address}: {response.status_code} - {response.text}"
                    )
                    return False

        except Exception as e:
            logger.error(f"Error reporting IP {ip_address}: {str(e)}")
            return False

    async def get_blacklist(
        self, confidence_minimum: int = 90, limit: int = 100
    ) -> list:
        """
        Get list of blacklisted IPs from AbuseIPDB

        Args:
            confidence_minimum: Minimum confidence score (0-100)
            limit: Maximum number of results

        Returns:
            List of blacklisted IP addresses
        """
        try:
            if not self.api_key:
                logger.warning(
                    "Cannot get blacklist - AbuseIPDB API key not configured"
                )
                return []

            url = f"{self.base_url}/blacklist"
            params = {"confidenceMinimum": confidence_minimum, "limit": limit}

            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers, params=params)

                if response.status_code == 200:
                    data = response.json()
                    return data.get("data", [])
                else:
                    logger.error(
                        f"Failed to get blacklist: {response.status_code} - {response.text}"
                    )
                    return []

        except Exception as e:
            logger.error(f"Error getting blacklist: {str(e)}")
            return []
