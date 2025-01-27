"""Основной модуль программы.

Создаются экземпляры бота и диспетчера, подключаем роутер,
запускается бот с помощью FastApi lifespan в асинхронном режиме.
Подключается база данных, логика аутентификации и админка.
"""

import asyncio
from contextlib import asynccontextmanager
from typing import Any

from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware


from app.core.config import settings
from app.handlers.callbacks import router
from app.core.database import async_session_maker


# WEBHOOK_PATH = f'/bot/{settings.telegram.bot_token}'
# WEBHOOK_URL = f'{settings.webhook_host}{WEBHOOK_PATH}'
# WEBHOOK_MODE = settings.telegram.webhook_mode

# bot = Bot(token=settings.telegram.bot_token, parse_mode='HTML')
# dp = Dispatcher()
# dp.update.middleware(DBSessionMiddleware(session_pool=async_session_maker))
# dp.callback_query.middleware(CallbackAnswerMiddleware())
# dp.include_router(router)


async def main():
    bot = Bot(token=settings.telegram.bot_token.get_secret_value())
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    print(str(settings.telegram.bot_token))
    # print(settings.db.url)


if __name__ == "__main__":
    asyncio.run(main())
