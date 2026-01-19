from sqlalchemy import ForeignKey, String, TIMESTAMP,func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    reason: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )
    