from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, date, timedelta
from typing import Optional
from app.models.activity import Activity


class StatsCRUD:
    @staticmethod
    async def get_category_stats(
        session: AsyncSession,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> list:
        """Получить сырые данные по категориям"""
        query = select(
            Activity.category,
            func.sum(Activity.duration_seconds).label('total_seconds'),
            func.count(Activity.id).label('count')
        )
        if start_date:
            query = query.where(Activity.start_time >= start_date)
        if end_date:
            query = query.where(
                Activity.end_time <= end_date + timedelta(days=1))

        query = query.group_by(Activity.category)

        result = await session.execute(query)
        return list(result.all())

    @staticmethod
    async def get_daily_stats(
        session: AsyncSession,
        start_date: datetime,
        end_date: datetime
    ) -> list:
        """Получить сырые данные по дням"""
        query = select(
            func.date(Activity.start_time).label('day'),
            Activity.category,
            func.sum(Activity.duration_seconds).label('total_seconds')
        ).where(
            Activity.start_time >= start_date
        ).group_by(
            'day', Activity.category
        ).order_by('day')
        result = await session.execute(query)
        return list(result.all())

    @staticmethod
    async def get_top_apps(
        session: AsyncSession,
        limit: int = 10,
        category: Optional[str] = None
    ) -> list:
        """Получить топ приложений"""
        query = select(
            Activity.app_name,
            func.sum(Activity.duration_seconds).label('total_seconds'),
            func.count(Activity.id).label('sessions')
        )
        if category:
            query = query.where(Activity.category == category)

        query = query.group_by(Activity.app_name).order_by(
            func.sum(Activity.duration_seconds).desc()
        ).limit(limit)

        result = await session.execute(query)
        return list(result.all())
