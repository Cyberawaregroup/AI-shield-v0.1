import logging
import typing

import orjson as json
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.services.base import Service, ServiceError, ServiceStatus
from app.core import security, utils
from app.core.utils import build_conditions
from app.db.threat_intelligence import BreachExposure
from app.db.users import User


class UserService(Service):
    id = "users"
    name = "Users"

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

    async def list_users(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        logger: typing.Optional[typing.Any] = None,
        **filters: typing.Any,
    ) -> list[User]:
        logger = logger or self.logger
        conditions = build_conditions(filters, User)
        query = (
            sa.select(User)
            .where(*conditions, ~User.is_deleted)
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(query)
        users = result.scalars().all()

        if logger:
            logger.info(f"Listed {len(users)} users with filters: {filters}")
        return list(users)

    async def count_users(
        self,
        session: AsyncSession,
        logger: typing.Optional[typing.Any] = None,
        **filters: typing.Any,
    ) -> int:
        logger = logger or self.logger
        conditions = build_conditions(filters, User)
        query = (
            sa.select(sa.func.count())
            .select_from(User)
            .where(*conditions, ~User.is_deleted)
        )
        result = await session.execute(query)
        count = result.scalar_one()

        if logger:
            logger.info(f"User count: {count} with filters: {filters}")
        return count

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

    async def create_user(
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
                logger.warning(f"User creation failed: Email already exists - {email}")
            raise ServiceError(
                "User with this email already exists",
                self.name,
                http_status=400,
            )

        user = User(
            email=email,
            name=name,
            role=role,
            age=age,
            phone=phone,
            vulnerability_factors="[]"
            if vulnerability_factors is None
            else json.dumps(vulnerability_factors).decode(),
        )
        user.hashed_password = security.get_password_hash(password)
        session.add(user)
        await session.flush()

        if logger:
            logger.info(f"User created successfully: {email}")
        return user

    async def update_user(
        self,
        session: AsyncSession,
        user_id: int,
        logger: typing.Optional[typing.Any] = None,
        **updates: typing.Any,
    ) -> User:
        logger = logger or self.logger
        result = await session.execute(
            sa.select(User)
            .where(User.id == user_id, ~User.is_deleted)
            .with_for_update()
        )
        user = result.scalar_one_or_none()

        if user is None:
            if logger:
                logger.warning(f"User update failed: User not found - {user_id}")
            raise ServiceError("User not found", self.name, http_status=404)

        for key, value in updates.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)

        user.updated_at = utils.now()
        await session.flush()

        if logger:
            logger.info(f"User updated successfully: {user.id}")
        return user

    async def delete_user(
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
                logger.warning(f"User deletion failed: User not found - {user_id}")
            raise ServiceError("User not found", self.name, http_status=404)

        # Soft delete - mark as deleted instead of removing from database
        user.is_deleted = True
        await session.flush()

        if logger:
            logger.info(f"User soft-deleted successfully: {user.email}")

    async def update_vulnerability_score(
        self,
        session: AsyncSession,
        user_id: int,
        vulnerability_score: float,
        is_vulnerable: bool | None = None,
        logger: typing.Optional[typing.Any] = None,
    ) -> User:
        logger = logger or self.logger
        result = await session.execute(
            sa.select(User)
            .where(User.id == user_id, ~User.is_deleted)
            .with_for_update()
        )
        user = result.scalar_one_or_none()

        if user is None:
            if logger:
                logger.warning(
                    f"Vulnerability update failed: User not found - {user_id}"
                )
            raise ServiceError("User not found", self.name, http_status=404)

        user.vulnerability_score = vulnerability_score
        if is_vulnerable is not None:
            user.is_vulnerable = is_vulnerable

        user.updated_at = utils.now()
        await session.flush()

        if logger:
            logger.info(f"Vulnerability score updated for user: {user.email}")
        return user

    async def update_risk_score(
        self,
        session: AsyncSession,
        user_id: int,
        risk_score: float,
        logger: typing.Optional[typing.Any] = None,
    ) -> User:
        logger = logger or self.logger
        result = await session.execute(
            sa.select(User)
            .where(User.id == user_id, ~User.is_deleted)
            .with_for_update()
        )
        user = result.scalar_one_or_none()

        if user is None:
            if logger:
                logger.warning(f"Risk score update failed: User not found - {user_id}")
            raise ServiceError("User not found", self.name, http_status=404)

        user.risk_score = risk_score
        user.updated_at = utils.now()
        await session.flush()

        if logger:
            logger.info(f"Risk score updated for user: {user.email}")
        return user

    async def increment_breach_count(
        self,
        session: AsyncSession,
        user_id: int,
        increment_by: int = 1,
        logger: typing.Optional[typing.Any] = None,
    ) -> User:
        logger = logger or self.logger
        result = await session.execute(
            sa.select(User)
            .where(User.id == user_id, ~User.is_deleted)
            .with_for_update()
        )
        user = result.scalar_one_or_none()

        if user is None:
            if logger:
                logger.warning(
                    f"Breach count update failed: User not found - {user_id}"
                )
            raise ServiceError("User not found", self.name, http_status=404)

        user.total_breaches += increment_by
        user.updated_at = utils.now()
        await session.flush()

        if logger:
            logger.info(f"Breach count incremented for user: {user.email}")
        return user

    async def increment_phishing_attempts(
        self,
        session: AsyncSession,
        user_id: int,
        increment_by: int = 1,
        logger: typing.Optional[typing.Any] = None,
    ) -> User:
        logger = logger or self.logger
        result = await session.execute(
            sa.select(User)
            .where(User.id == user_id, ~User.is_deleted)
            .with_for_update()
        )
        user = result.scalar_one_or_none()

        if user is None:
            if logger:
                logger.warning(
                    f"Phishing attempts update failed: User not found - {user_id}"
                )
            raise ServiceError("User not found", self.name, http_status=404)

        user.total_phishing_attempts += increment_by
        user.updated_at = utils.now()
        await session.flush()

        if logger:
            logger.info(f"Phishing attempts incremented for user: {user.email}")
        return user

    async def get_user_breaches(
        self,
        session: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        logger: typing.Optional[typing.Any] = None,
    ) -> list[BreachExposure]:
        logger = logger or self.logger
        query = (
            sa.select(BreachExposure)
            .where(BreachExposure.user_id == user_id, ~BreachExposure.is_deleted)
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(query)
        breaches = result.scalars().all()

        if logger:
            logger.info(f"Retrieved {len(breaches)} breaches for user ID: {user_id}")
        return list(breaches)

    async def get_vulnerable_users(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        logger: typing.Optional[typing.Any] = None,
    ) -> list[User]:
        logger = logger or self.logger
        query = (
            sa.select(User)
            .where(User.is_vulnerable.is_(True), ~User.is_deleted)
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(query)
        users = result.scalars().all()

        if logger:
            logger.info(f"Retrieved {len(users)} vulnerable users")
        return list(users)

    async def get_high_risk_users(
        self,
        session: AsyncSession,
        risk_threshold: float = 70.0,
        skip: int = 0,
        limit: int = 100,
        logger: typing.Optional[typing.Any] = None,
    ) -> list[User]:
        logger = logger or self.logger
        query = (
            sa.select(User)
            .where(User.risk_score >= risk_threshold, ~User.is_deleted)
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(query)
        users = result.scalars().all()

        if logger:
            logger.info(
                f"Retrieved {len(users)} high-risk users (threshold: {risk_threshold})"
            )
        return list(users)


user_service = UserService(logger=logging.getLogger(__name__))
