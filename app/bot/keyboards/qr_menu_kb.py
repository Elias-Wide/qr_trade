from datetime import datetime
from typing import TypeAlias

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.core.constants import (
    DEFAULT_KEYBOARD_SIZE,
    MONTH,
    POINT_LIST_KB_SIZE,
)
from app.bot.handlers.callbacks.menucallback import MenuCallBack
from app.bot.keyboards.buttons import (
    BACK_BTN,
    CANCEL,
    CANCEL_SEARCH,
    DELETE_QR,
    QR_BTN_TYPE,
    QR_MENU,
    SEND_QR,
)
from app.core.logging import logger
from app.points.models import Points
from app.sale_codes.dao import SaleCodesDAO
from app.users.models import Users

KeyboardMarkup: TypeAlias = InlineKeyboardMarkup | ReplyKeyboardMarkup


async def get_qr_list_kb(
    *,
    menu_name: str,
    next_menu: str,
    level: int = 0,
    size: int = DEFAULT_KEYBOARD_SIZE,
    btns_data: tuple[tuple[str]] | None = None,
    point_id: int | None = None,
    user_id: int | None = None,
    previous_menu: str = QR_MENU,
    code_id: int | None = None,
    trade_id: int | None = None,
    need_back_btn: bool = True,
) -> list[InlineKeyboardButton]:
    """
    Создание клавиатуры списка кодов пользователя.
    Применяется в меню удаления и отправки кодов.
    В первом случае объекты модели SaleCodes,
    где аттрибут file_name == 'deleted' помечаются доп. символами.
    Во втором случае объекта модели с таким атрибутом 'скипаются',
    т.к. нужны только объекты кодов, где загружено фото.
    """
    logger(menu_name)
    kb_builder = InlineKeyboardBuilder()
    btns = []
    user_codes = await SaleCodesDAO.get_actual_objs(
        attr_name="user_id", attr_value=user_id, need_actual=False
    )
    for code in user_codes:
        created_at = code.created_at
        created_at = f"{created_at.day} {MONTH[created_at.month]}"
        text = QR_BTN_TYPE[menu_name].format(code.client_id)
        if code.created_at != datetime.now().date():
            if menu_name == SEND_QR:
                continue
            elif menu_name == DELETE_QR:
                text = text[:-1] + "⚠️"
        btns.append(
            InlineKeyboardButton(
                text=text,
                callback_data=MenuCallBack(
                    code_id=code.id,
                    trade_id=trade_id,
                    user_id=user_id,
                    point_id=point_id,
                    level=level,
                    menu_name=next_menu,
                ).pack(),
            )
        )
    btns.append(
        InlineKeyboardButton(
            text=BACK_BTN,
            callback_data=MenuCallBack(
                level=level - 1,
                menu_name=QR_MENU,
                point_id=point_id,
                user_id=user_id,
            ).pack(),
        )
    )
    kb_builder.row(*btns, width=size)
    return kb_builder.as_markup()


async def get_point_list_kb(
    *,
    user_id: int,
    next_menu: str,
    level: int = 2,
    points_in_state: list,
    size: int = POINT_LIST_KB_SIZE,
    points_list: list[Points],
    previous_menu: str = QR_MENU,
) -> list[InlineKeyboardButton]:
    """
    Создание клавиатуры списка пунктов.
    """
    kb_builder = InlineKeyboardBuilder()
    btns = []
    for point in points_list:
        if point.point_id in points_in_state:
            continue
        text = f"🛍 {point.name}"
        btns.append(
            InlineKeyboardButton(
                text=text,
                callback_data=MenuCallBack(
                    user_id=user_id,
                    level=level,
                    point_id=point.point_id,
                    menu_name=next_menu,
                ).pack(),
            )
        )
    btns.append(
        InlineKeyboardButton(
            text=CANCEL_SEARCH,
            callback_data=MenuCallBack(
                level=level - 1, menu_name=CANCEL, user_id=user_id
            ).pack(),
        )
    )
    kb_builder.row(*btns, width=size)
    return kb_builder.as_markup()
