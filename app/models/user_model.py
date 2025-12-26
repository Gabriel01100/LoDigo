from sqlalchemy import BigInteger, Text, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.posts_model import Posts


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    anon_key: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    role: Mapped[str] = mapped_column(Text, default="user")
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )
    posts: Mapped[list["Posts"]] = relationship("Posts", back_populates="user")

