from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from fastapi import HTTPException

from app.models.posts_model import Posts
from app.models.report_model import Report
from app.models.school_model import School


class ModerationService:

    @staticmethod
    async def report_post(post_id: int, reason: str, user_id: int, session: AsyncSession):
        
        #validar que el post exista
        result = await session.execute(select(Posts).where(Posts.id == post_id, Posts.is_deleted == False))
        post = result.scalar_one_or_none()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        #si post duplicaod
        duplicate = await session.execute(select(Report).where(and_(Report.post_id ==post_id, Report.user_id == user_id)))
        
        if duplicate.scalar_one_or_none():
            raise HTTPException(
            status_code=400,
            detail="Post ya reportado"
        )

        report = Report(post_id = post_id, reason = reason, user_id = user_id)
        
        session.add(report)
        await session.commit()
        await session.refresh(report)

        return {"message": "Post reported successfully"}
    
    @staticmethod
    async def soft_delete_post(post_id: int, session: AsyncSession):
        result = await session.execute(
            select(Posts).where(Posts.id == post_id)
        )
        post = result.scalar_one_or_none()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        if post.is_deleted:
            raise HTTPException(
                status_code=400,
                detail="Post already hidden"
            )

        post.is_deleted = True
        await session.commit()

        return {"message": "Post hidden successfully"}
    
    @staticmethod
    async def restore_post(post_id: int, session: AsyncSession):
        result = await session.execute(
            select(Posts).where(Posts.id == post_id)
        )
        post = result.scalar_one_or_none()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        if not post.is_deleted:
            raise HTTPException(
                status_code=400,
                detail="Post is not hidden"
            )

        post.is_deleted = False
        await session.commit()

        return {"message": "Post restored successfully"}
    
    @staticmethod
    async def list_reports(session: AsyncSession):
        result = await session.execute(
        select(
            Posts.id,
            Posts.title,
            Posts.content,
            Posts.created_at,
            Posts.is_deleted,
            School.name.label("school_name"),
            func.count(Report.id).label("reports_count")
        )
        .join(Report, Report.post_id == Posts.id)
        .join(School, School.id == Posts.school_id, isouter=True)
        .group_by(Posts.id, School.name)
        .order_by(func.count(Report.id).desc())
    )


        # result = await session.execute(
        #     select(Report)
        #     .order_by(Report.created_at.desc())
        # )

        return result.all()