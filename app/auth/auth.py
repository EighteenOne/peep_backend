from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

from app.config.settings import settings

api_key_header = APIKeyHeader(name="X-API-Key")


def check_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == settings.API_KEY:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid API key"
    )
