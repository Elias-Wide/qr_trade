from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto

from app.bot.constants import NO_CAPTION, QR_SEND, QR_UPDATE
from app.bot.keyboards.buttons import CHECK_QR, DELETE_QR, QR_MENU, QR_MENU_BTNS, QR_SEND_BTNS
from app.bot.keyboards.main_menu_kb import get_image_and_kb
from app.bot.keyboards.qr_menu_kb import get_qr_delete_kb


from app.core.logging import get_logger
from app.bot.banners import captions, get_img
from app.sale_codes.dao import Sale_CodesDAO


async def get_qr_menu(
    level: int, menu_name: str, user_id: int, point_id: int
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Получить пользовательское меню."""
    match level:
        case 0:
            return await get_image_and_kb(
                menu_name=QR_MENU,
                user_id=user_id,
                btns_data=QR_MENU_BTNS,
                caption=NO_CAPTION,
                level=level,
                point_id=point_id,
            )
        case 1:
            if menu_name == DELETE_QR:
                user_codes = await Sale_CodesDAO.get_actual_objs(
                    attr_name="user_id", attr_value=user_id
                    )
                if not user_codes:
                    caption = captions.no_qr_today
                else:
                    caption = captions.del_qr
                return (
                    await get_img(menu_name, caption=caption),
                    await get_qr_delete_kb(user_id=user_id, level=level),
                )
            elif menu_name == QR_SEND:
                return await get_image_and_kb(
                    menu_name=QR_SEND,
                    user_id=user_id,
                    btns_data=QR_SEND_BTNS,
                    caption=captions.send_qr,
                    level=level + 1,
                    point_id=point_id,
                )
            elif menu_name == QR_UPDATE:   
                pass


async def get_qr_side_menu(
    level: int,
    menu_name: str,
    user_id: int,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    pass


async def get_qr_delete_btn(menu_name, user_id, level):
    pass
