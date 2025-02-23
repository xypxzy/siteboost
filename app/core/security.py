from datetime import datetime, timedelta
from typing import Any, Optional, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT access token
    :param subject: Token subject (usually user ID)
    :param expires_delta: Token expiration time
    :return: Encoded JWT token
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.utcnow() + expires_delta

    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def create_refresh_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT refresh token
    :param subject: Token subject (usually user ID)
    :param expires_delta: Token expiration time
    :return: Encoded JWT token
    """
    if expires_delta is None:
        expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    expire = datetime.utcnow() + expires_delta

    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify plain password against hashed password
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password
    """
    return pwd_context.hash(password)


def decode_token(token: str) -> dict:
    """
    Decode and verify JWT token
    :param token: JWT token
    :return: Decoded token payload
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.JWTError as e:
        raise ValueError(f"Invalid token: {str(e)}")


def verify_token_type(token: dict, expected_type: str) -> bool:
    """
    Verify token type (access or refresh)
    """
    return token.get("type") == expected_type


class SecurityUtils:
    @staticmethod
    def is_token_expired(token: dict) -> bool:
        """
        Check if token is expired
        """
        exp = token.get("exp")
        if not exp:
            return True
        return datetime.utcfromtimestamp(exp) < datetime.utcnow()

    @staticmethod
    def get_token_expiration(token: dict) -> Optional[datetime]:
        """
        Get token expiration datetime
        """
        exp = token.get("exp")
        if not exp:
            return None
        return datetime.utcfromtimestamp(exp)

    @staticmethod
    def create_tokens_for_user(user_id: str) -> dict:
        """
        Create both access and refresh tokens for user
        """
        access_token = create_access_token(subject=user_id)
        refresh_token = create_refresh_token(subject=user_id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # in seconds
            "refresh_expires_in": settings.REFRESH_TOKEN_EXPIRE_DAYS
            * 24
            * 60
            * 60,  # in seconds
        }

    @staticmethod
    def refresh_access_token(refresh_token: str) -> dict:
        """
        Create new access token using refresh token
        """
        payload = decode_token(refresh_token)

        if not verify_token_type(payload, "refresh"):
            raise ValueError("Invalid token type")

        if SecurityUtils.is_token_expired(payload):
            raise ValueError("Refresh token has expired")

        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Invalid token payload")

        access_token = create_access_token(subject=user_id)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        }
