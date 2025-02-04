"""Клавиатура вступительной анкеты."""

from typing import Iterable

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.constants import CONFIRM, DEFAULT_KEYBOARD_SIZE, MAIN_MENU


async def create_registration_kb(
    size: tuple[int] = DEFAULT_KEYBOARD_SIZE,
) -> InlineKeyboardMarkup | ReplyKeyboardMarkup:
    """Создать клавиутуру вступительной анкеты."""
    keyboard = InlineKeyboardBuilder()
    for text, callback_datas in zip(dict(CONFIRM).values(), dict(CONFIRM).keys()):
        keyboard.add(
            InlineKeyboardButton(text=text, callback_data=callback_datas),
        )
    return keyboard.adjust(*size).as_markup()


async def create_back_to_menu_kb(
    size: tuple[int] = DEFAULT_KEYBOARD_SIZE,
) -> InlineKeyboardMarkup | ReplyKeyboardMarkup:
    """Создать клавиутуру вступительной анкеты."""
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="ЗА РАБОТУ!!!!", callback_data=MAIN_MENU)
        )
    return keyboard.adjust(*size).as_markup()
    