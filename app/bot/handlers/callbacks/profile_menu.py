from aiogram.types import FSInputFile, InlineKeyboardMarkup, InputMediaPhoto

from app.bot.constants import MAIN_MENU, NO_IMAGE
from app.bot.keyboards.buttons import PROFILE, PROFILE_MENU_BTNS
from app.bot.keyboards.main_menu_kb import get_image_and_kb
from app.bot.utils import get_user_data
from app.core.config import STATIC_DIR

from app.core.logging import get_logger
from app.bot.banners import get_img
from app.users.dao import UsersDAO
from app.users.models import Users


async def get_profile_menu(
    level: int, menu_name: str, user_id: int, point_id: int
) -> tuple[InputMediaPhoto | str, InlineKeyboardMarkup]:
    """Получить пользовательское меню."""
    match level:
        case 1:
            user_data = await get_user_data(user_id)
            return await get_image_and_kb(
                menu_name=menu_name,
                user_id=user_id,
                level=level,
                btns_data=PROFILE_MENU_BTNS,
                caption=user_data,
                point_id=point_id,
                previous_menu=MAIN_MENU,
            )
