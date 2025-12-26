from sqlalchemy import BigInteger, Text, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user_model import User
    from app.models.school_model import School


from .base import Base

class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str | None] = mapped_column(Text)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )
    updated_at: Mapped[str] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    #FK

    user_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE")
    )

    school_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("schools.id")
    )
    user: Mapped["User"] = relationship("User", back_populates="posts")
    school: Mapped["School"] = relationship("School", back_populates="posts")