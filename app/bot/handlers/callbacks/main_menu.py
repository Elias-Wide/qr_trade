"""Модуль главного и других меню."""

from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InlineKeyboardMarkup,
    InputMediaPhoto,
)

from app.bot.banners import get_img
from app.bot.keyboards.main_menu_kb import get_main_menu_btns
from app.users.models import Users


async def get_main_menu(
    level: int, menu_name: str, user_id: int
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Возвращает главное меню."""
    return (
        await get_img(menu_name, level),
        await get_main_menu_btns(user_id=user_id, level=level),
    )
