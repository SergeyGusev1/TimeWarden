from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import List

from app.services.category_detector import AppCategory


class ActivityCreate(BaseModel):
    app_name: str
    window_title: str
    category: AppCategory = AppCategory.UNKNOWN
    duration_seconds: float
    start_time: datetime
    end_time: datetime


class ActivityResponse(ActivityCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ActivityList(BaseModel):
    items: List[ActivityResponse]
    total: int
    page: int
    size: int
