from fastapi import APIRouter, Request, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

from app.services.auth_service import AuthService


# Importar los templates cargados en main.py
from app.main import templates

router = APIRouter(prefix="/auth", tags=["Auth"]) 

@router.post("/login")
def login(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "title": "Iniciar Sesión"}
    )

@router.get("/me")
async def auth_me(request: Request, response:Response, session: AsyncSession = Depends(get_db)):
    user = await AuthService.get_or_create_anon_user(request, response, session)
    return {"status": "ok", "message": "Usuario anonimo reconocido", "role": user.role}
