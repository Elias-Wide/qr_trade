"""Модуль функций обработчиков для меню QR."""

from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto

from app.bot.constants import (
    DEFAULT_KEYBOARD_SIZE,
    DELETE_CODE,
    MAIN_MENU,
    MONTH,
    NO_CAPTION
)
from app.bot.handlers.callbacks.menucallback import MenuCallBack
from app.bot.keyboards.buttons import (
    DELETE_QR,
    DELETE_QR_BTN,
    POINT_SEARCH,
    QR_MENU,
    QR_MENU_BTNS,
    SEND_QR,
)
from app.bot.keyboards.main_menu_kb import get_image_and_kb

from app.core.config import QR_DIR
from app.bot.keyboards.banners import captions, get_img
from app.sale_codes.dao import Sale_CodesDAO
from app.sale_codes.models import Sale_Codes
from app.trades.dao import TradesDAO
from app.trades.models import Trades


async def get_qr_menu(
    level: int, menu_name: str, user_id: int, point_id: int, trade_id: int, code_id: int
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Получить пользовательское меню."""
    next_menu = None
    match level:
        case 1:
            menu_name = QR_MENU
            btns_data = QR_MENU_BTNS
            caption = NO_CAPTION
            previous_menu = MAIN_MENU
        case 2:
            btns_data = QR_MENU_BTNS
            caption = NO_CAPTION
            previous_menu = QR_MENU
            point_id = None
            if menu_name == DELETE_QR:
                menu_name = DELETE_QR
                btns_data = None
                next_menu = DELETE_CODE
            elif menu_name == SEND_QR:
                btns_data = None
                next_menu = POINT_SEARCH
                point_id = None

    return await get_image_and_kb(
        menu_name=menu_name,
        next_menu=next_menu,
        user_id=user_id,
        point_id=point_id,
        code_id=code_id,
        btns_data=btns_data,
        level=level,
        caption=caption,
        previous_menu=previous_menu,
    )


# async def get_sale_codes_data(
#     user_id: int, menu_name: str, btn_text: str,
# ) -> tuple[str, tuple[str, str] | None]:
#     """Получить описание данные для кнопок.
#     Запрос в бд возвращает список объектов
#     заданной модели по id юзера.
#     """
#     user_codes = await Sale_CodesDAO.get_actual_objs(
#         attr_name="user_id", attr_value=user_id, need_actual=True
#     )
#     btns_data = None
#     if user_codes:
#         for obj in user_codes:
#             created_at = obj.created_at
#             created_at = f"{created_at.day} {MONTH[created_at.month]}"
#             btns_data = tuple(
#                 (menu_name, btn_text.format(obj.value, created_at)) for obj in user_codes
#         )
#         caption = captions.delete_qr
#     else:
#         caption = captions.no_qr_today
#         btns_data = None
#     return caption, btns_data, code.


async def get_reply_no_trade(callback_data: MenuCallBack):
    """Получить"""
    if callback_data.point_id == 1:
        caption = captions.no_user_point
    else:
        caption = captions.point_no_qr
    return await get_image_and_kb(
        menu_name="point_no_qr",
        user_id=callback_data.user_id,
        level=callback_data.level,
        previous_menu=QR_MENU,
        caption=caption,
    )


async def get_reply_for_trade(callback_data: MenuCallBack, trade: Trades):
    """Получить изображение и клавиатуру для трейда."""

    return (
        await get_img(
            menu_name=trade.file_name, file_dir=QR_DIR, caption=captions.confirm_trade
        ),
        await get_trade_confirm_kb(
            level=callback_data.level,
            user_id=callback_data.user_id,
            point_id=callback_data.point_id,
            trade_id=trade.id,
        ),
    )
