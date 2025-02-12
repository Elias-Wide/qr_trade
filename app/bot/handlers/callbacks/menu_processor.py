"""Модуль главного и других меню."""

from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto

from app.bot.handlers.callbacks.faq_menu import get_faq_menu
from app.bot.handlers.callbacks.qr_menu import get_qr_menu
from app.core.logging import get_logger
from app.bot.constants import MAIN_MENU, QR_SEND
from app.bot.handlers.callbacks.main_menu import get_main_menu
from app.bot.handlers.callbacks.profile_menu import get_profile_menu
from app.bot.keyboards.buttons import (
    CHECK_QR,
    DELETE_QR,
    FAQ_MENU,
    FAQ_PROFILE,
    FAQ_QR,
    PROFILE,
    QR_MENU,
)


logger = get_logger(__name__)


async def get_menu_content(
    level: int, menu_name: str, user_id: int, point_id: int | None = None
) -> tuple[InputMediaPhoto | str, InlineKeyboardMarkup]:
    """Возвращает контент в зависимости от menu_name."""
    print(menu_name, level)
    if menu_name in (QR_MENU, CHECK_QR, DELETE_QR, QR_SEND):
        return await get_qr_menu(level, menu_name, user_id, point_id)
    elif menu_name in (FAQ_MENU, FAQ_PROFILE, FAQ_QR):
        return await get_faq_menu(level, menu_name, user_id)
    elif menu_name == PROFILE:
        return await get_profile_menu(level, menu_name, user_id, point_id)
    elif menu_name == MAIN_MENU:
        return await get_main_menu(level, menu_name, user_id)
