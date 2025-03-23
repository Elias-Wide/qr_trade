"""Основной модуль программы.

Создаются экземпляры бота и диспетчера, подключаем роутер,
запускается бот с помощью FastApi lifespan в асинхронном режиме.
Подключается база данных, логика аутентификации и админка.
"""

from aiogram.types import Update
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
import logging
from sqladmin import Admin
import uvicorn

from app.admin.adminview import admin_views
from app.admin.auth import authentication_backend
from app.bot.create_bot import bot, dp, stop_bot, start_bot

from app.bot.handlers.routers import main_router
from app.bot.handlers.registration_handlers import registration_router
from app.bot.keyboards.main_kb_builder import set_main_menu
from app.bot.scheduler import (
    clear_user_schedule,
    expire_old_sale_codes,
    delete_old_trades,
    send_order_notification,
)
from app.core.config import settings
from app.core.database import engine
from app.users.constants import NOTIFICATION_TIME, SCHEDULE_JOB_HOUR

WEBHOOK_PATH = f"/bot/{settings.telegram.bot_token.get_secret_value()}"
WEBHOOK_URL = f"{settings.telegram.webhook_host}/webhook"


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting bot setup...")
    scheduler = AsyncIOScheduler()
    scheduler.start()
    scheduler.add_job(
        send_order_notification,
        trigger="cron",
        hour=NOTIFICATION_TIME,
    )
    scheduler.add_job(
        clear_user_schedule,
        trigger="cron",
        day=1,
        hour=0,
        minute=0,
    )

    dp.include_router(main_router)
    dp.include_router(registration_router)
    await start_bot()
    await bot.set_webhook(
        url=WEBHOOK_URL,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )
    logging.info(f"Webhook set to {WEBHOOK_URL}")
    await set_main_menu(bot)
    yield
    logging.info("Shutting down bot...")
    await bot.delete_webhook()
    await stop_bot()
    logging.info("Webhook deleted")


app = FastAPI(lifespan=lifespan)


@app.post("/webhook")
async def webhook(request: Request) -> None:
    logging.info("Received webhook request")
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    logging.info("Update processed")


admin = Admin(
    app=app,
    engine=engine,
    authentication_backend=authentication_backend,
)

for view in admin_views:
    admin.add_view(view)
