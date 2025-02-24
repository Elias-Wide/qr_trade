"""Модуль главного и других меню."""

from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto

from app.bot.handlers.callbacks.faq_menu import get_faq_menu
from app.bot.handlers.callbacks.qr_menu import get_qr_menu
from app.bot.keyboards.main_menu_kb import get_image_and_kb
from app.bot.constants import MAIN_MENU
from app.bot.handlers.callbacks.profile_menu import get_profile_menu
from app.bot.keyboards.buttons import (
    CHECK_QR,
    DELETE_QR,
    FAQ_MENU,
    FAQ_PROFILE,
    FAQ_QR,
    MAIN_MENU_BUTTONS,
    NOTIFICATIONS,
    PROFILE,
    QR_MENU,
    SEND_QR,
)
from app.core.logging import logger

async def get_main_menu(
    level: int, menu_name: str, user_id: int, point_id: int | None = None
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Возвращает главное меню."""
    logger()
    return await get_image_and_kb(
        menu_name=menu_name,
        user_id=user_id,
        point_id=point_id,
        btns_data=MAIN_MENU_BUTTONS,
        level=level,
    )


async def get_menu_content(
    level: int,
    menu_name: str,
    user_id: int,
    point_id: int | None = None,
    trade_id: int | None = None,
    code_id: int | None = None,
) -> tuple[InputMediaPhoto | str, InlineKeyboardMarkup]:
    """Возвращает контент в зависимости от menu_name."""
    logger(level, menu_name, user_id, point_id, trade_id, code_id)
    if menu_name in (QR_MENU, CHECK_QR, DELETE_QR, SEND_QR):
        return await get_qr_menu(level, menu_name, user_id, point_id, trade_id, code_id)
    elif menu_name in (FAQ_MENU, FAQ_PROFILE, FAQ_QR):
        return await get_faq_menu(level, menu_name, user_id)
    elif menu_name in (PROFILE, NOTIFICATIONS):
        return await get_profile_menu(level, menu_name, user_id, point_id)
    elif menu_name == MAIN_MENU:
        return await get_main_menu(level, menu_name, user_id, point_id)
