from core.config import API_KEY, API_KEY_NAME
from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader


api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    if api_key == API_KEY:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials."
    )
