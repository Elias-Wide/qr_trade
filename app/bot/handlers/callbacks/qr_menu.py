"""Модуль функций обработчиков для меню QR."""

from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto

from app.core.constants import (
    DELETE_CODE,
    MAIN_MENU,
    NO_CAPTION,
)
from app.bot.handlers.callbacks.menucallback import MenuCallBack
from app.bot.keyboards.buttons import (
    CONFIRM_BTNS,
    DELETE_QR,
    POINT_SEARCH,
    QR_MENU,
    QR_MENU_BTNS,
    SEND_QR,
)
from app.bot.keyboards.banners import captions, get_img, get_qr_code_image
from app.bot.keyboards.main_kb_builder import get_btns, get_image_and_kb
from app.core.config import QR_DIR
from app.core.logging import logger
from app.sale_codes.dao import SaleCodesDAO
from app.sale_codes.models import SaleCodes
from app.trades.dao import TradesDAO
from app.trades.models import Trades


async def get_qr_menu(
    level: int,
    menu_name: str,
    user_id: int,
    point_id: int,
    trade_id: int,
    code_id: int,
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


async def get_reply_no_trade(
    callback_data: MenuCallBack,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Получить изображение и клавиаутуру, когда нет заказов на пункт"""
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
        need_back_btn=True,
    )


async def get_reply_for_trade(
    callback_data: MenuCallBack, trade: Trades
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Получить изображение и клавиатуру для трейда."""
    try:
        return (
            await get_qr_code_image(
                client_id=trade.client_id, encoded_value=trade.encoded_value
            ),
            await get_btns(
                level=callback_data.level,
                btns_data=CONFIRM_BTNS,
                menu_name=callback_data.menu_name,
                user_id=callback_data.user_id,
                point_id=callback_data.point_id,
                trade_id=trade.id,
                need_back_btn=False,
            ),
        )
    except Exception as error:
        logger(error)
        raise error
