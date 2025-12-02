import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    UserInfoResponse,
)
from app.api.v1.services.auth import auth_service
from app.api.v1.services.base import ServiceError
from app.core.db import get_session
from app.core.security import get_user


logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/login", response_model=LoginResponse, summary="User login endpoint")
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_session)):
    try:
        user = await auth_service.authenticate_user(
            session=db,
            email=login_data.email,
            password=login_data.password,
            logger=logger,
        )
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = await auth_service.create_access_token(
            data={"sub": str(user.id), "email": user.email},
            logger=logger,
        )
        await auth_service.update_last_login(
            session=db,
            user_id=user.id,
            logger=logger,
        )
        await db.commit()
        return LoginResponse(
            access_token=access_token, user_id=user.id, email=user.email
        )

    except ServiceError as e:
        await db.rollback()
        raise e.as_http_exception()
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Login failed"
        ) from e


@router.post(
    "/register", response_model=LoginResponse, summary="User registration endpoint"
)
async def register(
    register_data: RegisterRequest, db: AsyncSession = Depends(get_session)
):
    try:
        user = await auth_service.register_user(
            session=db,
            email=register_data.email,
            name=register_data.name,
            password=register_data.password,
            logger=logger,
        )
        access_token = await auth_service.create_access_token(
            data={"sub": str(user.id), "email": user.email},
            logger=logger,
        )
        await db.commit()

        return LoginResponse(
            access_token=access_token, user_id=user.id, email=user.email
        )

    except ServiceError as e:
        await db.rollback()
        raise e.as_http_exception()
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed",
        ) from e


@router.get("/me", response_model=UserInfoResponse, summary="Get current user info")
async def get_user_info(current_user=Depends(get_user)):
    return UserInfoResponse(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        role=current_user.role,
    )
