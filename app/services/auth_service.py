import secrets
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Request, Response

from app.models.user_model import User
from app.config import COOKIE_NAME


class AuthService:

    @staticmethod
    async def get_or_create_anon_user(request: Request,response: Response, session: AsyncSession) -> User:
        anon_key = request.cookies.get(COOKIE_NAME)
        if not anon_key:
            anon_key = secrets.token_hex(32)#64 chars
            response.set_cookie(
                key=COOKIE_NAME,
                value=anon_key,
                httponly=True,
                secure=False,   # True en producción
                samesite="lax",
                max_age=60 * 60 * 24 * 365,
            )
        #Buscarlo en la db
        result = await session.execute(select(User).where(User.anon_key == anon_key))
        user = result.scalar_one_or_none()

        #si no existe el uesr crearlo
        if not user:
            user=User(anon_key=anon_key)
            session.add(user)
            await session.commit()
            await session.refresh(user)
        
        return user