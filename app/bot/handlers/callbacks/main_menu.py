"""Модуль главного и других меню."""

from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InlineKeyboardMarkup,
    InputMediaPhoto,
)

from app.bot.banners import get_img
from app.bot.constants import MAIN_MENU
from app.bot.keyboards.buttons import MAIN_MENU_BUTTONS
from app.bot.keyboards.main_menu_kb import get_image_and_kb
from app.users.models import Users


async def get_main_menu(
    level: int, menu_name: str, user_id: int, point_id: int | None = None
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Возвращает главное меню."""
    return await get_image_and_kb(menu_name, user_id, point_id, MAIN_MENU_BUTTONS, level=level)
