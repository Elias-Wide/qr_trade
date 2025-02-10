"""Модуль главного и других меню."""

from typing import Optional
from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto

from app.bot.handlers.callbacks.faq_menu import get_faq_menu
from app.bot.handlers.callbacks.qr_menu import get_qr_menu
from app.core.logging import get_logger
from app.bot.constants import MAIN_MENU
from app.bot.handlers.callbacks.main_menu import get_main_menu
from app.bot.handlers.callbacks.profile_menu import get_profile_menu
from app.bot.keyboards.buttons import ADD_QR, CHECK_QR, DELETE_QR, FAQ_MENU, FAQ_PROFILE, FAQ_QR, PROFILE, QR_MENU


logger = get_logger(__name__)

MENU_NAME = {
    PROFILE: get_profile_menu,
    MAIN_MENU: get_main_menu,
    QR_MENU: get_qr_menu,
    ADD_QR: get_qr_menu,
    DELETE_QR: get_qr_menu,
    CHECK_QR: get_qr_menu,
    FAQ_MENU: get_faq_menu,
    FAQ_PROFILE: get_faq_menu,
    FAQ_QR: get_faq_menu,
}


async def get_menu_content(
    level: int,
    menu_name: str,
    user_id: int,
    code_id: int | None = None,
) -> tuple[InputMediaPhoto | str, InlineKeyboardMarkup]:
    """Возвращает контент в зависимости от menu_name."""
    print(menu_name, level)
    if menu_name in (QR_MENU, ADD_QR, CHECK_QR, DELETE_QR):
        return await get_qr_menu(level=level, menu_name=menu_name, user_id=user_id, code_id=code_id)
    elif menu_name in (FAQ_MENU, FAQ_PROFILE, FAQ_QR):
        return await get_faq_menu(level=level, menu_name=menu_name, user_id=user_id)
    elif menu_name == PROFILE:
        return await get_profile_menu(level=level, menu_name=menu_name, user_id=user_id)
    elif menu_name == MAIN_MENU:
        return await get_main_menu(level=level, menu_name=menu_name, user_id=user_id)
        
