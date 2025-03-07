from aiogram import Router

from app.bot.filters import BanFilter
from app.bot.handlers.other_handlers import echo_router
from app.bot.handlers.profile_handlers import profile_router
from app.bot.handlers.qr_menu_handlers import code_router
from app.bot.handlers.user_handlers import user_router
from app.bot.handlers.other_handlers import ban_router

main_router = Router()
main_router.message.filter(BanFilter())

main_router.include_routers(
    user_router, code_router, profile_router, echo_router
)
