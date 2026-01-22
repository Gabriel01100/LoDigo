from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.posts_model import Posts
from app.schemas.posts_schema import PostCreate, PostUpdate
from app.models.user_model import User

from app.utils.sanitizer import sanitize_text


class PostService:

    @staticmethod
    async def create_post(data:PostCreate, user:User, session:AsyncSession):
        #post = Posts(**data.model_dump(), user_id=user.id)
        post = Posts(
            title=sanitize_text(data.title) if data.title else None,
            content=sanitize_text(data.content),
            school_id=data.school_id,
            user_id=user.id
        )


        session.add(post)
        await session.commit()
        await session.refresh(post)
        return post

    @staticmethod
    async def list_posts(session:AsyncSession):
        result = await session.execute(select(Posts))
        return result.scalars().all()
    
    @staticmethod
    async def list_by_school(school_id:int, session:AsyncSession):
        result = await session.execute(select(Posts).where(Posts.school_id==school_id))
        return result.scalars().all()
    
    @staticmethod
    async def update_post(post_id:int, data:PostUpdate, user:User, session:AsyncSession):
        result = await session.execute(select(Posts).where(Posts.id == post_id).order_by(Posts.created_at.desc()))
        post = result.scalar_one_or_none()

        if not post or post.user_id != user.id:
            return None #probablemente Posts.user_id
        
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(post, k, v)
        
        await session.commit()
        await session.refresh(post)
        return post
    
    @staticmethod
    async def delete_post(post_id: int, user:User,session:AsyncSession):
        result = await session.execute(select(Posts).where(Posts.id == post_id))
        post = result.scalar_one_or_none()
        #cuando se muestra un solo objeto usar scalar_one_or_none
        if not post or post.user_id != user.id:
            raise HTTPException(status_code=403, detail="Usuario no autorizado o post no encotrado")
        
        await session.delete(post)
        await session.commit()
        return {"status": "ok", "message": "Post eliminado"}

