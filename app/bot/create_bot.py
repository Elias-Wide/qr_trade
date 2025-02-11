import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.core.config import settings


bot = Bot(
    token=settings.telegram.bot_token.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()


async def start_bot():
    try:
        await bot.send_message(settings.telegram.admin_id, f"Я запущен🥳.")
    except:
        print("СОБЩЕНИЕ НЕ ОТПРАВЛЕНО")


async def stop_bot():
    try:
        await bot.send_message(settings.telegram.admin_id, "Бот остановлен. За что?😔")
    except:
        pass


async def critical_message_to_admin(message: str):
    try:
        await bot.send_message(settings.telegram.admin_id, message)
    except:
        pass

# async def download_file(file, destination):
#     file_name = 
#     destination_file = await bot.download_file(file.file_id, os.path.join(os.getcwd(), file_name))
