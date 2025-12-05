"""
Authentication API router for JWT token generation.

Provides endpoint for obtaining JWT tokens for API access.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from app.auth import JWTManager
from app.utils.logger import logger

router = APIRouter(prefix="/v1/auth", tags=["auth"])


class LoginRequest(BaseModel):
    """Login request model."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response model."""

    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest) -> TokenResponse:
    """
    Generate JWT token for API access.

    In a production environment, you would validate credentials against a database.
    This is a simplified example for demonstration.

    Args:
        request: Login credentials (email and password).

    Returns:
        TokenResponse: JWT token for subsequent requests.
    """
    try:
        # TODO: In production, validate credentials against a user database
        # This is a simplified example - always grants token
        jwt_manager = JWTManager()

        token = jwt_manager.create_token(data={"sub": request.email})

        logger.info(f"Token generated for user: {request.email}")

        return TokenResponse(access_token=token)

    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate token"
        )
