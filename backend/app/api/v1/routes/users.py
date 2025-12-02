import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.users import (
    BreachResponse,
    UserCreate,
    UserCreateResponse,
    UserDeleteResponse,
    UserResponse,
    UserUpdate,
    UserUpdateResponse,
)
from app.api.v1.services.base import ServiceError
from app.api.v1.services.users import user_service
from app.core.db import get_session

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=list[UserResponse], summary="List users")
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_session),
):
    try:
        users = await user_service.list_users(
            session=db,
            skip=skip,
            limit=limit,
            logger=logger,
        )
        return [UserResponse.model_validate(user) for user in users]
    except ServiceError as e:
        raise e.as_http_exception()
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch users") from e


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    try:
        user = await user_service.get_user_by_id(
            session=db,
            user_id=user_id,
            logger=logger,
        )
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return UserResponse.model_validate(user)
    except ServiceError as e:
        raise e.as_http_exception()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch user") from e


@router.post("/", response_model=UserCreateResponse, summary="Create a new user")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_session)):
    try:
        db_user = await user_service.create_user(
            session=db,
            email=user.email,
            name=user.name,
            password=user.password.get_secret_value(),
            role=user.role,
            age=user.age,
            phone=user.phone,
            vulnerability_factors=user.vulnerability_factors or [],
            logger=logger,
        )
        await db.commit()
        return UserCreateResponse(
            id=db_user.id,
            email=db_user.email,
            name=db_user.name,
            role=db_user.role,
            message="User created successfully",
        )
    except ServiceError as e:
        await db.rollback()
        raise e.as_http_exception()
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create user") from e


@router.put("/{user_id}", response_model=UserUpdateResponse, summary="Update a user")
async def update_user(
    user_id: int, user_update: UserUpdate, db: AsyncSession = Depends(get_session)
):
    try:
        updates = user_update.model_dump(exclude_unset=True)
        db_user = await user_service.update_user(
            session=db,
            user_id=user_id,
            logger=logger,
            **updates,
        )
        await db.commit()
        
        return UserUpdateResponse(
            id=db_user.id,
            email=db_user.email,
            name=db_user.name,
            role=db_user.role,
            message="User updated successfully",
        )
    except ServiceError as e:
        await db.rollback()
        raise e.as_http_exception()
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update user") from e


@router.delete("/{user_id}", response_model=UserDeleteResponse, summary="Delete a user")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    try:
        await user_service.delete_user(
            session=db,
            user_id=user_id,
            logger=logger,
        )
        await db.commit()

        return UserDeleteResponse(message="User deleted successfully")
    except ServiceError as e:
        await db.rollback()
        raise e.as_http_exception()
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete user") from e


@router.get(
    "/{user_id}/breaches",
    response_model=list[BreachResponse],
    summary="Get user breaches",
)
async def get_user_breaches(user_id: int, db: AsyncSession = Depends(get_session)):
    try:
        breaches = await user_service.get_user_breaches(
            session=db,
            user_id=user_id,
            logger=logger,
        )
        return [BreachResponse.model_validate(breach) for breach in breaches]
    except ServiceError as e:
        raise e.as_http_exception()
    except Exception as e:
        logger.error(f"Error fetching breaches for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch user breaches")
