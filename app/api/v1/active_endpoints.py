from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.activity import ActivityCreate, ActivityResponse, ActivityList
from app.core.database import get_async_session
from app.services.activity_service import ActivityService
from app.crud.activity import ActivityCRUD


router = APIRouter()


@router.post('/api/activity', response_model=ActivityResponse)
async def activity_from_agent(
    activity_data: ActivityCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Принимает запись о активности от агента"""
    return await ActivityService.create_activity(session, activity_data)


@router.get('/api/activity/{activity_id}', response_model=ActivityResponse)
async def activity_by_id(
    activity_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Получить запись о активности по id"""
    return await ActivityCRUD.get_by_id(session, activity_id)


@router.get('/api/activity', response_model=ActivityList)
async def get_list_activity(
    session: AsyncSession = Depends(get_async_session),
    page: int = Query(1, ge=1, description='Номер страницы'),
    size: int = Query(10, ge=1, description='Размер страницы')
):
    """Получает список актитвностей с пагинацией"""
    activities, total = await ActivityService.get_list_activity(
        session, page, size)

    return ActivityList(
        items=[ActivityResponse.model_validate(act) for act in activities],
        total=total,
        page=page,
        size=size
    )
