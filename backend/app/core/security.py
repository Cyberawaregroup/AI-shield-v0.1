from datetime import datetime, timedelta, timezone
import logging
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_session
from app.db.users import User

logger = logging.getLogger(__name__)

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    :param plain_password: Plain text password
    :param hashed_password: Hashed password
    :return: True if password matches, False otherwise
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Error verifying password: {str(e)}")
        return False


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.

    :param password: Plain text password
    :return: Hashed password
    :raises HTTPException: If hashing fails
    """
    try:
        return pwd_context.hash(password)
    except Exception as e:
        logger.error(f"Error hashing password: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing password",
        )


def create_access_token(
    data: dict,
    expires_delta: Optional[int] = None,
    token_use: str = "access",
) -> str:
    """
    Create a new JWT access token.

    :param data: Data to encode in the token
    :param expires_delta: Token expiration time in minutes
    :param token_use: Token use type (e.g., 'access', 'refresh')
    :return: JWT access token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire, "token_use": token_use})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_access_token(token: str, expected_token_use: str = "access") -> dict:
    """
    Verify and decode a JWT access token.

    :param token: JWT access token
    :param expected_token_use: Expected token use type for validation
    :return: Decoded token payload
    :raises HTTPException: If token is invalid, expired, or has wrong token_use
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        token_use = payload.get("token_use")
        if token_use != expected_token_use:
            logger.error(
                f"Token use mismatch: expected '{expected_token_use}', got '{token_use}'"
            )
            raise credentials_exception

        return payload
    except JWTError as e:
        logger.error(f"JWT verification failed: {str(e)}")
        raise credentials_exception


async def get_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session),
) -> User:
    """
    Get the current authenticated and active user from JWT token.

    :param credentials: HTTP Bearer token credentials
    :param session: Database session
    :return: Current authenticated user
    :raises HTTPException: If authentication fails
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_access_token(credentials.credentials, expected_token_use="access")
    user_id: Optional[str] = payload.get("sub")

    if user_id is None:
        raise credentials_exception

    try:
        statement = select(User).where(User.id == int(user_id), ~User.is_deleted)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()

        if user is None:
            raise credentials_exception

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
            )
        return user

    except ValueError:
        logger.error(f"Invalid user_id format: {user_id}")
        raise credentials_exception
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting current user: {str(e)}")
        raise credentials_exception from e


async def get_admin(current_user: User = Depends(get_user)) -> User:
    """
    Get the current admin user.

    :param current_user: Current authenticated user
    :return: Current admin user
    :raises HTTPException: If user is not admin
    """
    if current_user.role not in ["admin", "it_director"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return current_user
