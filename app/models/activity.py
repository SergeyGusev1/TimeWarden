from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from datetime import datetime
from app.core.database import Base


class Activity(Base):
    __tablename__ = 'activities'

    id: Mapped[int] = mapped_column(primary_key=True)
    app_name: Mapped[str] = mapped_column(index=True)
    window_title: Mapped[str]
    category: Mapped[Optional[str]]
    duretion_seconds: Mapped[float]
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
