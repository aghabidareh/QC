import logging
from databases import Database
from sqlalchemy.exc import PendingRollbackError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from api.database.configs import (
    DATABASE_USERNAME,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_NAME,
    POOL_SIZE,
    MAX_OVERFLOW,
    POOL_TIMEOUT,
    POOL_RECYCLE,
)

logger = logging.getLogger(__name__)

DATABASE_URL = (
    f"postgresql+asyncpg://{DATABASE_USERNAME}:{DATABASE_PASSWORD}"
    f"@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    pool_size=POOL_SIZE,
    max_overflow=MAX_OVERFLOW,
    pool_timeout=POOL_TIMEOUT,
    pool_recycle=POOL_RECYCLE,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


