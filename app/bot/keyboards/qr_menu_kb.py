from typing import TypeAlias

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.constants import (
    DEFAULT_KEYBOARD_SIZE,
    DELETE_CODE,
    DELETE_QR_SIZE,
)
from app.bot.handlers.callbacks.menucallback import MenuCallBack
from app.bot.keyboards.buttons import (
    BACK_BTN,
    CHECK_QR,
    CONFIRM_BTNS,
    QR_MENU,
)
from app.sale_codes.dao import Sale_CodesDAO
from app.users.models import Users

KeyboardMarkup: TypeAlias = InlineKeyboardMarkup | ReplyKeyboardMarkup


async def get_qr_delete_kb(user_id: int, level: int, size: tuple[int] = DELETE_QR_SIZE):
    """Получить клавиатуру для удаления кода продажи."""
    user_codes = await Sale_CodesDAO.get_user_qr(user_id)
    keyboard = InlineKeyboardBuilder()
    for counter, code in enumerate(user_codes):
        keyboard.add(
            InlineKeyboardButton(
                text=f"❌ Удалить QR #{counter + 1} ({code.value}) ❌",
                callback_data=MenuCallBack(
                    code_id=code.id,
                    user_id=user_id,
                    level=level - 1,
                    menu_name=DELETE_CODE,
                ).pack(),
            )
        )
    keyboard.add(
        InlineKeyboardButton(
            text=BACK_BTN,
            callback_data=MenuCallBack(
                level=level - 1, menu_name=QR_MENU, user_id=user_id
            ).pack(),
        )
    )
    return keyboard.adjust(*size).as_markup()


async def get_trade_confirm_kb(
    *,
    level: int,
    user_id: int,
    point_id: int,
    trade_id: int, 
    size: tuple[int] = DEFAULT_KEYBOARD_SIZE,
    btns_data: dict[str] = CONFIRM_BTNS,
    previous_menu: str = QR_MENU,
    code_id: int | None = None,
) -> KeyboardMarkup:
    """
    Создание клавиатуры подтверждения продажи.
    Для этой клавиатуры параметр level не увеличиввается.
"""
    keyboard = InlineKeyboardBuilder()
    if btns_data:
        for menu_name, text in btns_data.items():
            keyboard.add(
                InlineKeyboardButton(
                    text=text,
                    callback_data=MenuCallBack(
                        level=level,
                        menu_name=menu_name,
                        user_id=user_id,
                        point_id=point_id,
                        code_id=code_id,
                        trade_id=trade_id
                    ).pack(),
                ),
            )

    keyboard.add(
        InlineKeyboardButton(
            text=BACK_BTN,
            callback_data=MenuCallBack(
                user_id=user_id,
                level=level - 1,
                menu_name=previous_menu,
                point_id=point_id,
            ).pack(),
        )
    )
    return keyboard.adjust(*size).as_markup()