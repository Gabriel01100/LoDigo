from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.config import settings


import app.models.user_model
import app.models.posts_model
import app.models.school_model

from app.models.base import Base

'''#Todos van a heredar de aca
class Base(DeclarativeBase):
    pass'''

DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_async_engine(DATABASE_URL,
                             echo=settings.DB_ECHO,
                             pool_pre_ping=True, #conexiones muertas
                             pool_size=5,
                             max_overflow=10)


AsyncSessionLocal = async_sessionmaker(engine,
                                       autoflush=False,
                                       expire_on_commit=False,
                                       autocommit=False)

'''async_session_factory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)
'''
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)