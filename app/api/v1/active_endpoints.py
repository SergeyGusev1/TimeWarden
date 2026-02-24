from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session


router = APIRouter()


@router.post('/api/activity')
async def activity_from_agent(
    session: AsyncSession = Depends(get_async_session)
):
    """Принимает запись о активности от агента"""
