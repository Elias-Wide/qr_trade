"""Основной модуль программы.

Создаются экземпляры бота и диспетчера, подключаем роутер,
запускается бот с помощью FastApi lifespan в асинхронном режиме.
Подключается база данных, логика аутентификации и админка.
"""

# import asyncio
# import uvicorn
# from contextlib import asynccontextmanager
# from typing import Any

# from aiogram import Bot, Dispatcher, types
# from aiogram.enums.parse_mode import ParseMode
# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.utils.callback_answer import CallbackAnswerMiddleware
# from fastapi import FastAPI
# from fastapi_sqlalchemy import DBSessionMiddleware


# from app.core.config import settings
# from app.handlers.callbacks import router
# from app.core.database import engine

# TG_TOKEN = settings.telegram.bot_token.get_secret_value()
# WEBHOOK_PATH = f'/bot/{TG_TOKEN}'
# WEBHOOK_URL = f'{settings.telegram.webhook_host}{WEBHOOK_PATH}'
# WEBHOOK_MODE = settings.telegram.webhook_mode

# bot = Bot(TG_TOKEN)
# dp = Dispatcher()
# dp.update.middleware(DBSessionMiddleware(engine))
# # dp.update.middleware(DBSessionMiddleware(session_pool=async_session_maker))
# dp.callback_query.middleware(CallbackAnswerMiddleware())
# dp.include_router(router)


# @asynccontextmanager
# async def lifespan(application: FastAPI) -> Any:
#     """Запуск бота в режиме webhook.

#     Добавление заданий в бота по отслеживанию
#     напоминаний о тренировках, сне, контроле калорий.
#     """
#     try:
#         await bot.set_webhook(
#             url=WEBHOOK_URL,
#             allowed_updates=dp.resolve_used_update_types(),
#             drop_pending_updates=True,
#         )
#         # logger.info('URL = %s', WEBHOOK_URL)
#     except Exception as e:
        
#         print(f"Can't set webhook - {e}")
#     yield
#     await bot.delete_webhook()
#     # logger.info("⛔ Stopping application")


# app = FastAPI(
#     lifespan=lifespan,
#     docs_url=None,
#     redoc_url=None,
# )
# app.add_middleware(DBSessionMiddleware, db_url=settings.db.url)


# @app.post(WEBHOOK_PATH)
# async def bot_webhook(update: dict) -> None:
#     """Назначаем путь для обработки POST-запросов от телеграмма."""
#     telegram_update = types.Update(**update)
#     await dp.feed_webhook_update(bot=bot, update=telegram_update)

import asyncio
import logging
from fastapi_sqlalchemy import DBSessionMiddleware
import uvicorn
from contextlib import asynccontextmanager
from app.bot.create_bot import bot, dp, stop_bot, start_bot
from app.bot.callbacks import router
from app.core.config import settings
from aiogram.types import Update
from fastapi import FastAPI, Request

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

WEBHOOK_PATH = f'/bot/{settings.telegram.bot_token.get_secret_value()}'
WEBHOOK_URL = f'{settings.telegram.webhook_host}/webhook'

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting bot setup...")
    dp.include_router(router)
    await start_bot()
    await bot.set_webhook(url=WEBHOOK_URL,
                          allowed_updates=dp.resolve_used_update_types(),
                          drop_pending_updates=True)
    logging.info(f"Webhook set to {WEBHOOK_URL}")
    yield
    logging.info("Shutting down bot...")
    await bot.delete_webhook()
    await stop_bot()
    logging.info("Webhook deleted")

    
app = FastAPI(lifespan=lifespan)
app.add_middleware(DBSessionMiddleware, db_url=settings.db.url)

# Маршрут для обработки вебхуков
@app.post("/webhook")
async def webhook(request: Request) -> None:
    logging.info("Received webhook request")
    update = await request.json()  # Получаем данные из запроса
    # Обрабатываем обновление через диспетчер (dp) и передаем в бот
    await dp.feed_update(bot, update)
    logging.info("Update processed")

async def main():
    config = uvicorn.Config("main:app", port=5000, log_level="info", reload=True)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())