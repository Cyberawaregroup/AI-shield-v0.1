from contextlib import asynccontextmanager, contextmanager
import logging
import typing

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import configure_mappers
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

logger = logging.getLogger(__name__)


engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=300,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_session(session_type: typing.Optional[typing.Type[Session]] = None, **kwargs):
    """
    Returns a new DB session.

    :param session_type: Type of session to return
    :param kwargs: Additional keyword arguments to pass to the session on creation
    """
    session_type_ = session_type or SessionLocal
    with session_type_(**kwargs) as session:
        yield session


######### ASYNC #########

async_engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=300,
)
AsyncSessionLocal = sessionmaker(  # type: ignore[arg-type]
    bind=async_engine,  # type: ignore[arg-type]
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)


@asynccontextmanager
async def get_async_session(
    session_type: typing.Optional[typing.Type[AsyncSession]] = None, **kwargs
):
    """
    Returns a new async DB session.

    :param session_type: Type of session to return
    :param kwargs: Additional keyword arguments to pass to the session on creation
    """
    session_type_ = session_type or AsyncSessionLocal
    async with session_type_(**kwargs) as session:  # type: ignore
        yield session


def bind_db_to_model_base(db_engine, model_base: DeclarativeMeta) -> None:
    """
    Bind the database engine to the model base, creating all tables in the database.
    """
    logger.info("Binding database engine to model base...")
    model_base.metadata.create_all(bind=db_engine)
    # Ensures that mappings/relationships between
    # models are properly defined on setup
    configure_mappers()
    logger.info("Database tables created and model base bound to engine.")


Base = declarative_base()
