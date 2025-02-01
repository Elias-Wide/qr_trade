"""Клавиатура вступительной анкеты."""

from typing import Iterable

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.constants import CONFIRM, DEFAULT_KEYBOARD_SIZE


async def create_registration_kb(
    items: Iterable[str],
    callback_datas: Iterable[str | None] = (None,),
    size: tuple[int] = DEFAULT_KEYBOARD_SIZE,
) -> InlineKeyboardMarkup | ReplyKeyboardMarkup:
    """Создать клавиутуру вступительной анкеты."""
    keyboard = InlineKeyboardBuilder()
    for text, callback_datas in zip(CONFIRM.values(), CONFIRM.keys()):
        keyboard.add(
            InlineKeyboardButton(text=text, callback_data=callback_datas),
        )
    return keyboard.adjust(*size).as_markup()
