from sqlalchemy.ext.asyncio import AsyncSession
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate
from app.services.category_detector import CategoryDetector, AppCategory
from app.crud.activity import ActivityCRUD


class ActivityService:
    @staticmethod
    async def create_activity(
        session: AsyncSession,
        activity_data: ActivityCreate
    ) -> Activity:
        detected_category = CategoryDetector.detect(
            activity_data.app_name,
            activity_data.window_title
        )
        final_category = activity_data.category
        if detected_category != AppCategory.UNKNOWN:
            final_category = detected_category

        return await ActivityCRUD.create(
            session,
            app_name=activity_data.app_name,
            window_title=activity_data.window_title,
            category=final_category,
            duration_seconds=activity_data.duration_seconds,
            start_time=activity_data.start_time,
            end_time=activity_data.end_time
        )

    @staticmethod
    async def get_list_activity(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[Activity], int]:
        """Получить список аксьтивностей с пагинацией. и их общее количество"""
        activities = await ActivityCRUD.get_list(session, skip, limit)
        total = await ActivityCRUD.count(session)
        return activities, total
