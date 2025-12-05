"""
JWT token management and authentication utilities.

This module handles JWT token creation, validation, and extraction.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import jwt
from app.config import get_settings


class JWTManager:
    """
    Manages JWT token operations: creation, validation, and decoding.

    Uses HS256 algorithm for signing tokens with configurable expiration.
    """

    def __init__(self):
        """Initialize JWT manager with settings."""
        self.settings = get_settings()

    def create_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT token with optional custom expiration.

        Args:
            data: Dictionary containing token claims (typically user info).
            expires_delta: Custom expiration time. If None, uses default from settings.

        Returns:
            str: Encoded JWT token.

        Example:
            >>> manager = JWTManager()
            >>> token = manager.create_token({"sub": "user@example.com"})
        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                hours=self.settings.jwt_expiration_hours
            )

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode, self.settings.jwt_secret_key, algorithm=self.settings.jwt_algorithm
        )

        return encoded_jwt

    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verify and decode a JWT token.

        Args:
            token: JWT token string to verify.

        Returns:
            Dict[str, Any]: Decoded token payload.

        Raises:
            jwt.ExpiredSignatureError: Token has expired.
            jwt.InvalidTokenError: Token is invalid or malformed.
        """
        try:
            payload = jwt.decode(
                token, self.settings.jwt_secret_key, algorithms=[self.settings.jwt_algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError("Token has expired")
        except jwt.InvalidTokenError:
            raise jwt.InvalidTokenError("Invalid token")

    def extract_token_from_header(self, authorization: str) -> str:
        """
        Extract JWT token from Authorization header.

        Args:
            authorization: Authorization header value (e.g., "Bearer <token>").

        Returns:
            str: Extracted JWT token.

        Raises:
            ValueError: If header format is invalid.
        """
        if not authorization or not authorization.startswith("Bearer "):
            raise ValueError("Invalid authorization header format")

        return authorization.split(" ")[1]
