"""Основной модуль программы.

Создаются экземпляры бота и диспетчера, подключаем роутер,
запускается бот с помощью FastApi lifespan в асинхронном режиме.
Подключается база данных, логика аутентификации и админка.
"""

import logging
from fastapi_sqlalchemy import DBSessionMiddleware
import uvicorn
from contextlib import asynccontextmanager
from app.bot.create_bot import bot, dp, stop_bot, start_bot
from app.bot.handlers.registration_handlers import registration_router
from app.bot.handlers.routers import main_router
from app.core.config import settings
from aiogram.types import Update
from fastapi import FastAPI, Request

from app.core.database import async_session_maker

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

WEBHOOK_PATH = f"/bot/{settings.telegram.bot_token.get_secret_value()}"
WEBHOOK_URL = f"{settings.telegram.webhook_host}/webhook"


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting bot setup...")
    dp.include_router(main_router)
    await start_bot()
    await bot.set_webhook(
        url=WEBHOOK_URL,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )
    logging.info(f"Webhook set to {WEBHOOK_URL}")
    yield
    logging.info("Shutting down bot...")
    await bot.delete_webhook()
    await stop_bot()
    logging.info("Webhook deleted")


app = FastAPI(lifespan=lifespan)


# Маршрут для обработки вебхуков
@app.post("/webhook")
async def webhook(request: Request) -> None:
    logging.info("Received webhook request")
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    logging.info("Update processed")


if __name__ == "__main__":
    config = uvicorn.Config("main:app", port=5000, log_level="info")
    server = uvicorn.Server(config)
    server.run()
