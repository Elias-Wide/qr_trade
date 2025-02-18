from typing import TypeAlias

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.constants import DEFAULT_KEYBOARD_SIZE, DELETE_CODE, MONTH
from app.bot.handlers.callbacks.menucallback import MenuCallBack
from app.bot.keyboards.buttons import (
    BACK_BTN,
    CHECK_QR,
    CONFIRM_BTNS,
    DELETE_QR_BTN,
    QR_MENU,
)
from app.sale_codes.dao import Sale_CodesDAO
from app.users.models import Users

KeyboardMarkup: TypeAlias = InlineKeyboardMarkup | ReplyKeyboardMarkup


async def get_qr_delete_kb(
    *,
    level: int = 0,
    size: int = DEFAULT_KEYBOARD_SIZE,
    btns_data: tuple[str, str] | None = None,
    point_id: int | None = None,
    user_id: int | None = None,
    previous_menu: str = QR_MENU,
    code_id: int | None = None,
    trade_id: int | None = None,
) -> list[InlineKeyboardButton]:
    """
    Создание клавиатуры.
    Текст кнопок и колбэк дата берется из констант.
    Если btns_data нет - создается только кнопка Назад.
    """
    kb_builder = InlineKeyboardBuilder()
    btns = []
    user_codes = await Sale_CodesDAO.get_user_qr(user_id)
    for code in user_codes:
        created_at = code.created_at
        created_at = f"{created_at.day} {MONTH[created_at.month]}"
        btns.append(
            InlineKeyboardButton(
                text=DELETE_QR_BTN.format(code.value, created_at),
                callback_data=MenuCallBack(
                    code_id=code.id,
                    trade_id=trade_id,
                    user_id=user_id,
                    point_id=point_id,
                    level=level,
                    menu_name=DELETE_CODE,
                ).pack(),
            )
        )
    btns.append(
        InlineKeyboardButton(
            text=BACK_BTN,
            callback_data=MenuCallBack(
                level=level - 1, menu_name=QR_MENU, point_id=point_id, user_id=user_id
            ).pack(),
        )
    )
    kb_builder.row(*btns, width=size)
    return kb_builder.as_markup()
