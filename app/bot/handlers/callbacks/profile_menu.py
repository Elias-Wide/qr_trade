from aiogram.types import FSInputFile, InlineKeyboardMarkup, InputMediaPhoto

from app.bot.constants import NO_IMAGE
from app.bot.keyboards.buttons import PROFILE, PROFILE_MENU_BTNS
from app.bot.keyboards.main_menu_kb import (
    get_image_and_kb,
    get_main_menu_btns,
    get_side_menu_btns,
)
from app.bot.utils import get_user_data
from app.core.config import STATIC_DIR

from app.core.logging import get_logger
from app.bot.banners import get_img
from app.users.dao import UsersDAO
from app.users.models import Users


async def get_profile_menu(
    level: int,
    menu_name: str,
    user_id: int,
) -> tuple[InputMediaPhoto | str, InlineKeyboardMarkup]:
    """Получить пользовательское меню."""
    user_data = await get_user_data(user_id)
    return await get_image_and_kb(
        menu_name=PROFILE,
        user_id=user_id,
        btns_data=PROFILE_MENU_BTNS,
        caption=user_data,
    )
