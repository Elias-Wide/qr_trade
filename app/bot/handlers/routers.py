from aiogram import Router

from app.bot.filters import BanFilter
from app.bot.handlers.admin_handlers import admin_router
from app.bot.handlers.other_handlers import echo_router
from app.bot.handlers.profile_handlers import profile_router
from app.bot.handlers.qr_menu_handlers import code_router
from app.bot.handlers.user_handlers import user_router


main_router = Router()
main_router.message.filter(BanFilter())

main_router.include_routers(
    admin_router, user_router, code_router, profile_router, echo_router
)
