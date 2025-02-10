from aiogram.types import FSInputFile, InlineKeyboardMarkup, InputMediaPhoto

from app.bot.constants import NO_IMAGE
from app.bot.keyboards.buttons import FAQ_MENU, FAQ_QR, FAQ_PROFILE, PROFILE, PROFILE_MENU_BTNS
from app.bot.keyboards.faq_kb import get_faq_kb, get_faq_side_menu_kb
from app.bot.keyboards.main_menu_kb import (
    get_image_and_kb,
    get_side_menu_btns,
)
from app.bot.utils import get_user_data
from app.core.config import STATIC_DIR

from app.core.logging import get_logger
from app.bot.banners import get_img
from app.users.dao import UsersDAO
from app.users.models import Users


async def get_faq_menu(
    level: int,
    user_id: int,
    menu_name: str
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Получить пользовательское меню."""
    image = await get_img(menu_name=menu_name, level=level)
    print(level)
    match level:
        case 0:
            keyboard = await get_faq_kb(user_id=user_id, level=level)
        case 1:
            keyboard = await get_faq_side_menu_kb(user_id=user_id, level=level)

    return (image, keyboard)