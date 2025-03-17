from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto

from app.core.constants import MAIN_MENU
from app.bot.keyboards.buttons import FAQ_MENU, FAQ_MENU_BTNS

from app.bot.keyboards.banners import get_img
from app.bot.keyboards.main_kb_builder import get_image_and_kb


async def get_faq_menu(
    level: int,
    menu_name: str,
    user_id: int,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Получить меню FAQ в зависимости от level."""
    match level:
        case 1:
            btns_data = FAQ_MENU_BTNS
            previous_menu = MAIN_MENU
        case 2:
            btns_data = None
            previous_menu = FAQ_MENU
    return await get_image_and_kb(
        menu_name=menu_name,
        user_id=user_id,
        btns_data=btns_data,
        level=level,
        previous_menu=previous_menu,
    )
