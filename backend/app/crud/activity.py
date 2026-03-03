from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate


class ActivityCRUD:
    @staticmethod
    async def create(
        session: AsyncSession,
        **kwargs
    ) -> Activity:
        """Создание записи в БД"""
        db_activity = Activity(**kwargs)
        session.add(db_activity)
        await session.commit()
        await session.refresh(db_activity)
        return db_activity

    @staticmethod
    async def get_by_id(
        session: AsyncSession,
        activity_id: int
    ) -> Activity | None:
        """Получение по id"""
        return await session.get(Activity, activity_id)

    @staticmethod
    async def count(session: AsyncSession) -> int:
        """Общее количество записей"""
        result = await session.execute(
            select(func.count()).select_from(Activity))
        return result.scalar() or 0

    @staticmethod
    async def get_list(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> list[Activity]:
        """Список с пагинацией"""
        result = await session.execute(
            select(Activity).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
