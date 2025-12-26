from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from app.models.school_model import School
from app.schemas.school_schema import SchoolCreate


class SchoolService:

    @staticmethod
    async def list_schools(session: AsyncSession):
        result = await session.execute(select(School))
        return result.scalars().all()
    
    @staticmethod
    async def create_school(data:SchoolCreate, session:AsyncSession):
        new_school = School(**data.model_dump())
        session.add(new_school)
        await session.commit()
        await session.refresh(new_school)
        return new_school