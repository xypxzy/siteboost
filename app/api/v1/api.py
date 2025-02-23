from fastapi import APIRouter
from app.api.v1.endpoints import analysis, auth
from app.core.config import settings


api_router = APIRouter()

# Auth routes
api_router.include_router(auth.router, tags=["authentication"])

# # User management
# api_router.include_router(users.router, prefix="/users", tags=["users"])

# # Website management
# api_router.include_router(websites.router, prefix="/websites", tags=["websites"])

# # Analysis
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])

# # Webhooks
# api_router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
