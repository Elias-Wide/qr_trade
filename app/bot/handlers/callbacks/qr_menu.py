from aiogram.types import FSInputFile, InlineKeyboardMarkup, InputMediaPhoto

from app.bot.constants import NO_IMAGE
from app.bot.keyboards.buttons import PROFILE, PROFILE_MENU_BTNS, QR_MENU, QR_MENU_BTNS
from app.bot.keyboards.main_menu_kb import (
    get_image_and_kb,
    get_main_menu_btns,
    get_side_menu_btns,
)
from app.bot.utils import get_user_data
from app.core.config import STATIC_DIR

from app.core.logging import get_logger
from app.bot.banners import captions, get_img
from app.sale_codes.dao import Sale_CodesDAO
from app.users.dao import UsersDAO


async def get_qr_menu(
    level: int,
    menu_name: str,
    user_id: int,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Получить пользовательское меню."""
    user_qr = await Sale_CodesDAO.get_user_qr(user_id)
    print(user_qr)
    if not user_qr:
        caption = captions.no_qr_today
    else:
        caption = captions.qr_today.format(f_qr=len(user_qr))  # await get_image_and_kb
    return await get_image_and_kb(
        menu_name=QR_MENU, user_id=user_id, btns_data=QR_MENU_BTNS, caption=caption
    )
