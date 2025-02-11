from typing import TypeAlias

from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    ReplyKeyboardMarkup,
)
from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.banners import get_img
from app.bot.constants import (
    DEFAULT_KEYBOARD_SIZE,
    DELETE_CODE,
    DELETE_QR_SIZE,
    MAIN_MENU,
    MAIN_MENU_COMMANDS,
    NO_IMAGE,
)
from app.bot.handlers.callbacks.menucallback import MenuCallBack
from app.bot.keyboards.buttons import BACK_BTN, DELETE_QR, FAQ_MENU, FAQ_MENU_BTNS, MAIN_MENU_BUTTONS, PROFILE, QR_MENU
from app.core.config import settings
from app.sale_codes.dao import Sale_CodesDAO
from app.users.models import Users

KeyboardMarkup: TypeAlias = InlineKeyboardMarkup | ReplyKeyboardMarkup


async def get_qr_delete_kb(user_id: int, level: int, size: tuple[int] = DELETE_QR_SIZE):
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
                ).pack()
            )
        )
    keyboard.add(
        InlineKeyboardButton(
            text=BACK_BTN,
            callback_data=MenuCallBack(
                level=level - 1,
                menu_name=QR_MENU,
                user_id=user_id
            ).pack()
        )
    )
    return keyboard.adjust(*size).as_markup()