from sqlalchemy import Column, Integer, String, Float, DateTime
from app.core.database import Base


class activity(Base):
    __tablename__='activities'

    id = Column(Integer, primary_key=True)
    app_name = Column(String, index=True)
    window_title = Column(String)
    category = Column(String, nullable=True)
    duretion_seconds = Column(Float)
    start_time = Column(DateTime)
    end_time = Column(DateTime)