from typing import Annotated, AsyncGenerator
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal, get_db
from app.models.user_model import User
from sqlalchemy import select

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

def require_role(allowed_roles: list[str]):
    async def _require_role(request : Request,session: AsyncSession = Depends(get_db))-> User:
            anon_key = request.cookies.get("anon_key")

            if not anon_key:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated"
                )
            
            result = await session.execute(select(User).where(User.anon_key == anon_key))
            user = result.scalar_one_or_none()

            if not user or user.role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Permission denied"
                )
            return user
    return _require_role