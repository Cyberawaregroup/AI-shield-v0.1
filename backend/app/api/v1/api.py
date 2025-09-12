from fastapi import APIRouter
from app.api.v1.endpoints import (
    users,
    threat_intelligence,
    fraud_reports,
    security_advisors,
    analytics,
    chatbot_simple as chatbot,
    auth
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(threat_intelligence.router, prefix="/threat-intelligence", tags=["threat-intelligence"])
api_router.include_router(fraud_reports.router, prefix="/fraud-reports", tags=["fraud-reports"])
api_router.include_router(security_advisors.router, prefix="/security-advisors", tags=["security-advisors"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])

# Health check endpoint
@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "threat-intelligence-api"}
