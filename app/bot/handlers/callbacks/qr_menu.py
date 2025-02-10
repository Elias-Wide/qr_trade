from aiogram.types import FSInputFile, InlineKeyboardMarkup, InputMediaPhoto

from app.bot.constants import NO_CAPTION, NO_IMAGE
from app.bot.keyboards.buttons import ADD_QR, CHECK_QR, DELETE_QR, PROFILE, PROFILE_MENU_BTNS, QR_MENU, QR_MENU_BTNS
from app.bot.keyboards.main_menu_kb import (
    get_image_and_kb,
    get_main_menu_btns,
    get_side_menu_btns,
)
from app.bot.keyboards.qr_menu_kb import get_qr_delete_kb
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
    code_id: int | None
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Получить пользовательское меню."""
    match level:
        case 0:
            return await get_image_and_kb(
                menu_name=QR_MENU,
                user_id=user_id,
                btns_data=QR_MENU_BTNS,
                caption=NO_CAPTION,
                level=level
            )
        case 1:
            user_codes = await Sale_CodesDAO.get_user_qr(user_id)
            if menu_name == DELETE_QR:
                if not user_codes:
                    caption = captions.no_qr_today
                else:
                    caption = captions.no_caption
                return (
                    await get_img(menu_name, caption=caption), 
                    await get_qr_delete_kb(user_id=user_id, level=level)
                )               
            
async def get_qr_side_menu(
    level: int,
    menu_name: str,
    user_id: int,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    pass

async def get_qr_delete_btn(menu_name, user_id, level):
    pass