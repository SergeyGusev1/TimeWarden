from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from typing import Optional

from app.core.database import get_async_session
from app.services.stats_service import StatsService


router = APIRouter()


@router.get('/categories', response_model=dict)
async def get_category_stats(
    start_date: Optional[date] = Query(None, description='Начальная дата'),
    end_date: Optional[date] = Query(None, description='Конечная дата'),
    session: AsyncSession = Depends(get_async_session)
):
    """Статистика по категориям за период"""
    return await StatsService.get_category_stats(session, start_date, end_date)


@router.get('/daily', response_model=list)
async def get_daily_stats(
    days: int = Query(7, ge=1, le=30, description='Количество дней'),
    session: AsyncSession = Depends(get_async_session)
):
    """Статистика по дням"""
    return await StatsService.get_daily_stats(session, days)


@router.get('/top-apps', response_model=list)
async def get_top_apps(
    limit: int = Query(10, ge=1, le=50, description='Количество приложений'),
    category: Optional[str] = Query(None, description='Фильтр по категории'),
    session: AsyncSession = Depends(get_async_session)
):
    """Топ приложений по времени использования"""
    return await StatsService.get_top_apps(session, limit, category)
