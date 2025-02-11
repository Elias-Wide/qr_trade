from aiogram import Router

from app.bot.handlers.other_handlers import echo_router
from app.bot.handlers.qr_menu_handlers import code_router
from app.bot.handlers.registration_handlers import registration_router
from app.bot.handlers.user_handlers import user_router

main_router = Router()

main_router.include_routers(registration_router, user_router, code_router, echo_router)
