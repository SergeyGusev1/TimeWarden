import asyncio
from datetime import datetime, time, timedelta
from app.core.database import AsyncSessionLocal
from app.services.telegram_service import TelegramNotifier


class Scheduler:
    def __init__(self):
        self.notifier = TelegramNotifier()
        self.running = False

    async def run_daily_at_21(self):
        """Запуск ежедневного отчёта в 21:00"""
        while self.running:
            now = datetime.now()
            target = datetime.combine(now.date(), time(21, 0))

            if now > target:
                target = datetime.combine(
                    now.date() + timedelta(days=1), time(21, 0))

            wait_seconds = (target - now).total_seconds()
            await asyncio.sleep(wait_seconds)

            async with AsyncSessionLocal() as session:
                await self.notifier.send_daily_report(session)

    async def run_periodic_checks(self):
        """Периодические проверки (каждый час)"""
        while self.running:
            await asyncio.sleep(3600)  # час

            async with AsyncSessionLocal() as session:
                await self.notifier.check_wasteful_alert(session)
                await self.notifier.congratulate_productive(session)

    async def start(self):
        """Запуск всех задач"""
        self.running = True
        await asyncio.gather(
            self.run_daily_at_21(),
            self.run_periodic_checks()
        )

    def stop(self):
        self.running = False
