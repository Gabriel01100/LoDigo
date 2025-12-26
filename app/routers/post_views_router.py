from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.post_service import PostService
from app.services.school_service import SchoolService
from app.core.templates import templates


router = APIRouter()

@router.get("/posts", response_class=HTMLResponse)
async def posts_view(
    request: Request,
    session: AsyncSession = Depends(get_db)
):
    posts = await PostService.list_posts(session)
    schools = await SchoolService.list_schools(session)

    return templates.TemplateResponse("post.html", {"request":request,"posts":posts, "school": schools})
