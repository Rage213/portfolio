from fastapi import Request, HTTPException, status
from fastapi.middleware.base import BaseHTTPMiddleware
from config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("analytics-api")

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Allow health checks and docs without API key
        if request.url.path in ["/health", "/docs", "/openapi.json", "/redoc"]:
            return await call_next(request)
            
        api_key = request.headers.get("X-API-Key")
        if not api_key or api_key != settings.API_KEY:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing X-API-Key header"
            )
            
        logger.info(f"Authorized request: {request.method} {request.url.path}")
        response = await call_next(request)
        return response
