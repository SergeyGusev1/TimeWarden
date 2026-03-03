from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, datetime, timedelta
from typing import Optional, Dict
from app.crud.stats import StatsCRUD


class StatsService:
    @staticmethod
    async def get_category_stats(
        session: AsyncSession,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> dict:
        """Статистика по категориям"""
        raw_stats = await StatsCRUD.get_category_stats(
            session, start_date, end_date)
        categories: Dict[str, Dict[str, float]] = {}
        total = 0.0

        for category, seconds, count in raw_stats:
            categories[category.value] = {
                'seconds': float(seconds),
                'count': count
            }
            total += seconds

        if total > 0:
            for cat in categories.values():
                cat['percentage'] = round(cat['seconds'] / total * 100, 1)

        return {
            'categories': categories,
            'total_seconds': float(total)
        }

    @staticmethod
    async def get_daily_stats(
        session: AsyncSession,
        days: int = 7
    ) -> list:
        """Статистика по дням"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        raw_stats = await StatsCRUD.get_daily_stats(
            session, start_date, end_date)
        daily_stats: dict[str, dict[str, float]] = {}
        for day, category, seconds in raw_stats:
            if day not in daily_stats:
                daily_stats[day] = {}
            daily_stats[day][category.value] = float(seconds)

        return [
            {"date": day, "categories": cats}
            for day, cats in daily_stats.items()
        ]

    @staticmethod
    async def get_top_apps(
        session: AsyncSession,
        limit: int = 10,
        category: Optional[str] = None
    ) -> list:
        """Топ приложений по времени"""
        raw_stats = await StatsCRUD.get_top_apps(session, limit, category)

        return [
            {
                "app_name": app_name,
                "total_seconds": float(seconds),
                "sessions": sessions,
                "hours": round(float(seconds) / 3600, 1)
            }
            for app_name, seconds, sessions in raw_stats
        ]
