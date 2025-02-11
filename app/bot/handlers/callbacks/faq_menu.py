from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto

from app.bot.keyboards.faq_kb import get_faq_kb, get_faq_side_menu_kb

from app.bot.banners import get_img


async def get_faq_menu(
    level: int,
    menu_name: str,
    user_id: int,
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
