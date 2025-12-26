from fastapi import APIRouter, Depends, Request, Response, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.security.rate_limits import rate_limits_posts
from app.database import get_db
#Schemas y servicios
from app.schemas.posts_schema import PostCreate, PostUpdate, PostResponse
from app.services.post_service import PostService
from app.services.auth_service import AuthService

from app.core.templates import templates



router = APIRouter(prefix="/posts", tags=["Posteo"])

@router.post("/", response_model=PostResponse, dependencies=[Depends(rate_limits_posts)])
async def create_post(data:PostCreate, request:Request, response:Response, session:AsyncSession=Depends(get_db)):
    user = await AuthService.get_or_create_anon_user(request, response, session)
    return await PostService.create_post(data, user, session)


@router.get("/", response_model=list[PostResponse])
async def list_posts(session: AsyncSession =Depends(get_db)):
    return await PostService.list_posts(session)

@router.get("/school/{school_id}", response_model=list[PostResponse])
async def list_posts_by_school(school_id:int,request: Request, session: AsyncSession = Depends(get_db),):
    posts = await PostService.list_by_school(school_id, session)

    return templates.TemplateResponse("post.html", {"request":request, "school_id": school_id})

@router.put("/{post_id}", response_model=PostResponse)
async def update_post(post_id:int, data:PostUpdate,request: Request, response: Response, session: AsyncSession = Depends(get_db)):

    user = await AuthService.get_or_create_anon_user(request, response, session)

    post = await PostService.update_post(post_id, data, user, session)

    if not post:
        raise HTTPException(status_code=404, detail="Error al editar")

    
    return post

@router.delete("/{post_id}")
async def delete_post(post_id: int,request: Request,response: Response,session: AsyncSession = Depends(get_db)):
    user = await AuthService.get_or_create_anon_user(request, response, session)
    result = await PostService.delete_post(post_id, user, session)


    if not result:
        raise HTTPException(status_code=404, detail="Error al borrar")

    return {"status": "ok"}

