from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates

from app.database import get_db
from app.dependecies import require_role
from app.services.moderation_service import ModerationService

router = APIRouter(prefix="/moderation", tags=["Moderation"])
templates= Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def moderation_panel(request: Request, moderator = Depends(require_role(["moderator"])), session : AsyncSession = Depends(get_db)):
    reports = await ModerationService.list_reports(session)

    return templates.TemplateResponse("moderation.html", {"request": request, "reports": reports})

                           

