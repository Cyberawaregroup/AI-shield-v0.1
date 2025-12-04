import logging
import typing

import orjson as json
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.base import Service, ServiceError, ServiceStatus
from app.core import security, utils
from app.core.utils import build_conditions
from app.db.users import User


class AuthService(Service):
    id = "auth"
    name = "Authentication"

    async def health_check(self, db: typing.Optional[AsyncSession]) -> ServiceStatus:
        try:
            if not db:
                raise ServiceError(
                    "Database session is not available.", self.name, http_status=503
                )
            await db.execute(sa.select(User).limit(1))
            return {
                "name": self.name,
                "status": "healthy",
                "error": None,
            }
        except Exception as exc:
            raise ServiceError(
                f"Health check failed for {self.name!r}: {str(exc)}",
                self.name,
                http_status=503,
            ) from exc

    async def create_access_token(
        self,
        data: dict,
        expires_delta: int | None = None,
        token_use: str = "access",
        logger: typing.Optional[typing.Any] = None,
    ) -> str:
        """
        Create access token using the security module.

        :param data: Token data
        :param expires_delta: Optional expiration time in minutes
        :param token_use: Token use type (e.g., 'access', 'refresh')
        :param logger: Optional logger instance
        :return: JWT access token
        """
        logger = logger or self.logger
        token = security.create_access_token(data, expires_delta, token_use)

        if logger:
            logger.info(f"Access token created for user: {data.get('email')}")
        return token

    async def verify_access_token(
        self,
        token: str,
        expected_token_use: str = "access",
        logger: typing.Optional[typing.Any] = None,
    ) -> dict:
        """
        Verify access token using the security module.

        :param token: JWT token to verify
        :param expected_token_use: Expected token use type
        :param logger: Optional logger instance
        :return: Decoded token payload
        :raises ServiceError: If token verification fails
        """
        logger = logger or self.logger
        try:
            payload = security.verify_access_token(token, expected_token_use)
            return payload
        except Exception as e:
            if logger:
                logger.error(f"Token verification failed: {str(e)}")
            raise ServiceError(
                "Invalid or expired token",
                "auth",
                http_status=401,
            ) from e

    async def authenticate_user(
        self,
        session: AsyncSession,
        email: str,
        password: str,
        logger: typing.Optional[typing.Any] = None,
    ) -> typing.Optional[User]:
        logger = logger or self.logger
        result = await session.execute(
            sa.select(User).where(User.email == email, ~User.is_deleted)
        )
        user = result.scalar_one_or_none()

        if user is None:
            if logger:
                logger.warning(f"Authentication failed: User not found - {email}")
            return None

        if not user.hashed_password or not security.verify_password(
            password, user.hashed_password
        ):
            if logger:
                logger.warning(f"Authentication failed: Invalid password - {email}")
            return None

        if logger:
            logger.info(f"User authenticated successfully: {email}")
        return user

    async def register_user(
        self,
        session: AsyncSession,
        email: str,
        name: str,
        password: str,
        role: str = "user",
        age: int | None = None,
        phone: str | None = None,
        vulnerability_factors: list[str] | None = None,
        logger: typing.Optional[typing.Any] = None,
    ) -> User:
        logger = logger or self.logger
        existing_user = await session.execute(
            sa.select(User).where(User.email == email, ~User.is_deleted)
        )
        if existing_user.scalar_one_or_none():
            if logger:
                logger.warning(f"Registration failed: Email already exists - {email}")
            raise ServiceError(
                "User with this email already exists",
                self.name,
                http_status=400,
            )

        user = User(
            email=email,
            name=name,
            role=role,
            age=age or 25,
            phone=phone,
            vulnerability_factors="[]"
            if vulnerability_factors is None
            else json.dumps(vulnerability_factors).decode(),
        )
        user.hashed_password = security.get_password_hash(password)
        session.add(user)
        await session.flush()

        if logger:
            logger.info(f"User registered successfully: {email}")
        return user

    async def check_user_exists(
        self,
        session: AsyncSession,
        email: str,
        logger: typing.Optional[typing.Any] = None,
    ) -> bool:
        logger = logger or self.logger
        result = await session.execute(
            sa.select(sa.exists().where(User.email == email))
        )
        exists = result.scalar_one()

        if logger:
            logger.debug(f"User exists check for {email}: {exists}")
        return exists

    async def retrieve_user(
        self,
        session: AsyncSession,
        logger: typing.Optional[typing.Any] = None,
        **filters: typing.Any,
    ) -> typing.Optional[User]:
        logger = logger or self.logger
        conditions = build_conditions(filters, User)
        query = sa.select(User).where(*conditions, ~User.is_deleted)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if logger and user is None:
            logger.warning(f"User not found with filters: {filters}")
        return user

    async def get_user_by_id(
        self,
        session: AsyncSession,
        user_id: int,
        logger: typing.Optional[typing.Any] = None,
    ) -> typing.Optional[User]:
        logger = logger or self.logger
        result = await session.execute(
            sa.select(User).where(User.id == user_id, ~User.is_deleted)
        )
        user = result.scalar_one_or_none()

        if logger and user is None:
            logger.warning(f"User not found with ID: {user_id}")
        return user

    async def get_user_by_email(
        self,
        session: AsyncSession,
        email: str,
        logger: typing.Optional[typing.Any] = None,
    ) -> typing.Optional[User]:
        logger = logger or self.logger
        result = await session.execute(
            sa.select(User).where(User.email == email, ~User.is_deleted)
        )
        user = result.scalar_one_or_none()

        if logger and user is None:
            logger.warning(f"User not found with email: {email}")
        return user

    async def update_last_login(
        self,
        session: AsyncSession,
        user_id: int,
        logger: typing.Optional[typing.Any] = None,
    ) -> None:
        logger = logger or self.logger
        result = await session.execute(
            sa.select(User)
            .where(User.id == user_id, ~User.is_deleted)
            .with_for_update()
        )
        user = result.scalar_one_or_none()

        if user is not None:
            user.updated_at = utils.now()
            await session.flush()

            if logger:
                logger.info(f"Updated last login for user: {user.email}")

    async def change_password(
        self,
        session: AsyncSession,
        user_id: int,
        old_password: str,
        new_password: str,
        logger: typing.Optional[typing.Any] = None,
    ) -> bool:
        logger = logger or self.logger
        result = await session.execute(
            sa.select(User)
            .where(User.id == user_id, ~User.is_deleted)
            .with_for_update()
        )
        user = result.scalar_one_or_none()

        if user is None:
            if logger:
                logger.warning(f"Password change failed: User not found - {user_id}")
            raise ServiceError("User not found", self.name, http_status=404)

        if not user.hashed_password or not security.verify_password(
            old_password, user.hashed_password
        ):
            if logger:
                logger.warning(
                    f"Password change failed: Invalid old password - {user.email}"
                )
            raise ServiceError("Invalid old password", self.name, http_status=400)

        user.hashed_password = security.get_password_hash(new_password)
        await session.flush()

        if logger:
            logger.info(f"Password changed successfully for user: {user.email}")
        return True

    async def deactivate_user(
        self,
        session: AsyncSession,
        user_id: int,
        logger: typing.Optional[typing.Any] = None,
    ) -> None:
        logger = logger or self.logger
        result = await session.execute(
            sa.select(User)
            .where(User.id == user_id, ~User.is_deleted)
            .with_for_update()
        )
        user = result.scalar_one_or_none()

        if user is None:
            if logger:
                logger.warning(f"Deactivation failed: User not found - {user_id}")
            raise ServiceError("User not found", self.name, http_status=404)

        user.is_active = False
        await session.flush()

        if logger:
            logger.info(f"User deactivated: {user.email}")

    async def activate_user(
        self,
        session: AsyncSession,
        user_id: int,
        logger: typing.Optional[typing.Any] = None,
    ) -> None:
        logger = logger or self.logger
        result = await session.execute(
            sa.select(User)
            .where(User.id == user_id, ~User.is_deleted)
            .with_for_update()
        )
        user = result.scalar_one_or_none()

        if user is None:
            if logger:
                logger.warning(f"Activation failed: User not found - {user_id}")
            raise ServiceError("User not found", self.name, http_status=404)

        user.is_active = True
        await session.flush()

        if logger:
            logger.info(f"User activated: {user.email}")


auth_service = AuthService(logger=logging.getLogger(__name__))
