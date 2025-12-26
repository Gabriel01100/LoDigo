from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.school_model import School
from app.schemas.school_schema import SchoolResponse, SchoolCreate

from app.services.school_service import SchoolService
from fastapi.templating import Jinja2Templates

from app.core.templates import templates


router = APIRouter(prefix="/schools", tags=["Schools"])

@router.get("/", response_model=list[SchoolResponse])
async def list_schools(session: AsyncSession = Depends(get_db)):
    return await SchoolService.list_schools(session)
    

#Para admin
@router.post("/", response_model=SchoolResponse)
async def create_school(data:SchoolCreate, session:AsyncSession=Depends(get_db)):
    return await SchoolService.create_school(data,session)

@router.get("/view")
async def schools_view(
    request: Request,
    session: AsyncSession = Depends(get_db)
):
    schools = await SchoolService.list_schools(session)

    return templates.TemplateResponse(
        "school.html",
        {
            "request": request,
            "schools": schools,
            "is_moderator": False  # Hacer admin
        }
    )