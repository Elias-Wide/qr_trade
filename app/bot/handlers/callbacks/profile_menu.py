from aiogram.types import FSInputFile, InlineKeyboardMarkup, InputMediaPhoto

from app.bot.constants import MAIN_MENU
from app.bot.keyboards.buttons import (
    NOTIFICATIONS,
    NOTIFICATIONS_BTNS,
    PROFILE,
    PROFILE_MENU_BTNS,
)
from app.bot.keyboards.main_kb_builder import get_image_and_kb
from app.bot.utils import get_notice_type, get_user_data
from app.core.logging import logger

from app.bot.keyboards.banners import get_img


async def get_profile_menu(
    level: int, menu_name: str, user_id: int, point_id: int
) -> tuple[InputMediaPhoto | str, InlineKeyboardMarkup]:
    """Получить пользовательское меню."""
    logger()
    match level:
        case 1:
            caption = await get_user_data(user_id)
            btns_data = PROFILE_MENU_BTNS
            previous_menu = MAIN_MENU
        case 2:
            if menu_name == NOTIFICATIONS:
                btns_data = NOTIFICATIONS_BTNS
                caption = await get_notice_type(user_id)
                previous_menu = PROFILE
    return await get_image_and_kb(
        menu_name=menu_name,
        user_id=user_id,
        level=level,
        btns_data=btns_data,
        caption=caption,
        point_id=point_id,
        previous_menu=previous_menu,
    )
