from enum import Enum


class ChatSessionStatus(str, Enum):
    ACTIVE = "active"
    ESCALATED = "escalated"
    CLOSED = "closed"
    ARCHIVED = "archived"

    def __str__(self) -> str:
        return self.value


class MessageType(str, Enum):
    USER = "user"
    BOT = "bot"
    ADVISOR = "advisor"
    SYSTEM = "system"

    def __str__(self) -> str:
        return self.value


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

    def __str__(self) -> str:
        return self.value


class FraudType(str, Enum):
    PHISHING = "phishing"
    SOCIAL_ENGINEERING = "social_engineering"
    IDENTITY_THEFT = "identity_theft"
    FINANCIAL_FRAUD = "financial_fraud"
    TECH_SUPPORT_SCAM = "tech_support_scam"
    ROMANCE_SCAM = "romance_scam"
    INVESTMENT_SCAM = "investment_scam"
    BANKING_SCAM = "banking_scam"
    OTHER = "other"

    def __str__(self) -> str:
        return self.value


class ThreatSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

    def __str__(self) -> str:
        return self.value


class IOCType(str, Enum):
    IP_ADDRESS = "ip_address"
    DOMAIN = "domain"
    URL = "url"
    EMAIL = "email"
    HASH = "hash"
    FILENAME = "filename"

    def __str__(self) -> str:
        return self.value


class ThreatSource(str, Enum):
    HIBP = "hibp"
    ABUSEIPDB = "abuseipdb"
    PHISHSCAN = "phishscan"
    SOCRADAR = "socradar"
    NETCRAFT = "netcraft"
    CLOUDFLARE = "cloudflare"
    MANUAL = "manual"

    def __str__(self) -> str:
        return self.value
