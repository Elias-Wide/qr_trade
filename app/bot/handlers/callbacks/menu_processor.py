"""Модуль главного и других меню."""

from typing import Optional
from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto

from app.bot.handlers.callbacks.qr_menu import get_qr_menu
from app.core.logging import get_logger
from app.bot.constants import MAIN_MENU
from app.bot.handlers.callbacks.main_menu import get_main_menu
from app.bot.handlers.callbacks.profile_menu import get_faq_menu, get_profile_menu
from app.bot.keyboards.buttons import FAQ_MENU, PROFILE, QR_MENU


logger = get_logger(__name__)

MENU_NAME = {
    PROFILE: get_profile_menu,
    MAIN_MENU: get_main_menu,
    QR_MENU: get_qr_menu,
    FAQ_MENU: get_faq_menu,
}


async def get_menu_content(
    level: int,
    menu_name: str,
    user_id: int,
) -> tuple[InputMediaPhoto | str, InlineKeyboardMarkup]:
    """Возвращает контент в зависимости от level и menu_name."""
    return await MENU_NAME[menu_name](level=level, menu_name=menu_name, user_id=user_id)
