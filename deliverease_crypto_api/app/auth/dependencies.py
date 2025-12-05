"""
Authentication middleware and dependencies for FastAPI.

Provides JWT validation middleware and dependency injection for protected routes.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.jwt_manager import JWTManager
import jwt

security = HTTPBearer()
jwt_manager = JWTManager()


async def verify_jwt(credentials=Depends(security)) -> dict:
    """
    Verify JWT token from HTTP Bearer authentication.

    This dependency validates JWT tokens in protected routes.

    Args:
        credentials: HTTP Bearer credentials from FastAPI security.

    Returns:
        dict: Decoded token payload containing user information.

    Raises:
        HTTPException: If token is invalid or expired.

    Example:
        @router.get("/protected")
        async def protected_route(current_user: dict = Depends(verify_jwt)):
            return {"user": current_user}
    """
    # credentials is an HTTPAuthorizationCredentials object
    token = credentials.credentials if hasattr(credentials, "credentials") else credentials

    try:
        payload = jwt_manager.verify_token(token)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user_id(current_user: dict = Depends(verify_jwt)) -> str:
    """
    Extract user ID from verified JWT token.

    Args:
        current_user: Decoded token payload from verify_jwt dependency.

    Returns:
        str: User identifier from token "sub" claim.

    Raises:
        HTTPException: If "sub" claim is missing.
    """
    user_id = current_user.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token claims",
        )
    return user_id
