from typing import Annotated, AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal

async def get_async_session() -> AsyncGenerator[AsyncSession,None]:
    """
    Dependencia que crea una sesión async de SQLAlchemy
    y la cierra automáticamente al finalizar el request.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()