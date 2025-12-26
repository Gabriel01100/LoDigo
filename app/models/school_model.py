from sqlalchemy import BigInteger, Text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.posts_model import Posts

from .base import Base

class School(Base):
    __tablename__ = "schools"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name:Mapped[str]= mapped_column(String, nullable=False)
    location:Mapped[str]= mapped_column(String,nullable=True)

    posts : Mapped[list["Posts"]] = relationship("Posts", back_populates="school")