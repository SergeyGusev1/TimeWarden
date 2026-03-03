import asyncio
from telegram import Bot
from telegram.error import TelegramError
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.crud.stats import StatsCRUD
from app.services.category_detector import AppCategory


class TelegramNotifier:
    def __init__(self):
        self.bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        self.chat_id = settings.TELEGRAM_CHAT_ID

    async def send_message(self, text: str) -> bool:
        """Отправить сообщение"""
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=text,
                parse_mode='HTML'
            )
            return True
        except TelegramError as e:
            print(f"Ошибка отправки в Telegram: {e}")
            return False

    async def send_daily_report(self, session: AsyncSession):
        """Ежедневный отчёт в 21:00"""
        today = datetime.now().date()
        stats = await StatsCRUD.get_category_stats(session, today, today)

        productive = 0
        neutral = 0
        wasteful = 0
        total = 0

        for category, seconds, count in stats:
            if category == AppCategory.PRODUCTIVE:
                productive = seconds
            elif category == AppCategory.NEUTRAL:
                neutral = seconds
            elif category == AppCategory.WASTEFUL:
                wasteful = seconds
            total += seconds

        message = f"📊 <b>Отчёт за {today}</b>\n\n"
        message += f"✅ Продуктивно: {productive/3600:.1f} ч\n"
        message += f"⚪ Нейтрально: {neutral/3600:.1f} ч\n"
        message += f"❌ Бесполезно: {wasteful/3600:.1f} ч\n"
        message += f"📈 Всего: {total/3600:.1f} ч\n\n"

        if total > 0:
            prod_percent = (productive / total) * 100
            message += f"🎯 Продуктивность: {prod_percent:.1f}%\n"

            if prod_percent > 70:
                message += "🔥 Отличный день!"
            elif prod_percent > 50:
                message += "👍 Неплохо, можно лучше"
            elif prod_percent > 30:
                message += "😐 Средненько"
            else:
                message += "😴 Завтра будет лучше"

        await self.send_message(message)

    async def check_wasteful_alert(self, session: AsyncSession):
        """Проверка на слишком много wasted времени"""
        today = datetime.now().date()
        stats = await StatsCRUD.get_category_stats(session, today, today)

        for category, seconds, count in stats:
            if category == AppCategory.WASTEFUL and seconds > 4 * 3600:
                message = (
                    f"⚠️ <b>Внимание!</b>\n\n"
                    f"Сегодня уже {seconds/3600:.1f} часов "
                    f"бесполезной активности!\n"
                    f"Может, поработаем? 💪"
                )
                await self.send_message(message)
                break

    async def congratulate_productive(self, session: AsyncSession):
        """Поздравление с достижением цели"""
        today = datetime.now().date()
        stats = await StatsCRUD.get_category_stats(session, today, today)

        for category, seconds, count in stats:
            if category == AppCategory.PRODUCTIVE and seconds >= 6 * 3600:
                message = (
                    f"🎉 <b>Цель достигнута!</b>\n\n"
                    f"Сегодня {seconds/3600:.1f} часов "
                    f"продуктивной работы!\n"
                    f"Ты красавчик! 🔥"
                )
                await self.send_message(message)
                break
