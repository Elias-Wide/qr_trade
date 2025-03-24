"""Модуль по созданию клавиатур в меню."""

from typing import TypeAlias

from aiogram.types import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    ReplyKeyboardMarkup,
)
from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards.qr_menu_kb import get_qr_list_kb
from app.bot.keyboards.banners import get_img
from app.core.constants import (
    DEFAULT_KEYBOARD_SIZE,
    MAIN_MENU,
    MAIN_MENU_COMMANDS,
)
from app.bot.handlers.callbacks.menucallback import MenuCallBack
from app.bot.keyboards.buttons import (
    BACK_BTN,
    DELETE_QR,
    FAQ_QR,
    SEND_QR,
)
from app.core.config import settings
from app.core.logging import logger


KeyboardMarkup: TypeAlias = InlineKeyboardMarkup | ReplyKeyboardMarkup


async def set_main_menu(bot: Bot) -> None:
    """Установить основное меню, назначить команды с описаниями."""
    main_menu_commands = [
        BotCommand(command=command, description=description)
        for command, description in MAIN_MENU_COMMANDS.items()
    ]
    await bot.set_chat_menu_button(menu_button=None)
    await bot.set_my_commands(main_menu_commands)


async def get_btns(
    *,
    menu_name: str,
    next_menu: str | None = None,
    level: int = 0,
    size: int = DEFAULT_KEYBOARD_SIZE,
    btns_data: tuple[str, str] | None = None,
    point_id: int | None = None,
    user_id: int | None = None,
    previous_menu: str = MAIN_MENU,
    code_id: int | None = None,
    trade_id: int | None = None,
    need_back_btn: bool = True,
) -> list[InlineKeyboardButton]:
    """
    Создание клавиатуры.
    Текст кнопок и колбэк дата берется из констант модуля buttons.
    Если btns_data нет - создается только кнопка Назад.
    """
    kb_builder = InlineKeyboardBuilder()
    btns = []
    if btns_data:
        logger(btns_data)
        for menu_name, text in btns_data:
            btns.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=MenuCallBack(
                        level=level + 1,
                        menu_name=menu_name,
                        user_id=user_id,
                        point_id=point_id,
                        code_id=code_id,
                        trade_id=trade_id,
                    ).pack(),
                ),
            )
        if menu_name == FAQ_QR:
            btns.append(admin_btn)
    if need_back_btn:
        btns.append(
            InlineKeyboardButton(
                text=BACK_BTN,
                callback_data=MenuCallBack(
                    user_id=user_id,
                    level=level - 1,
                    point_id=point_id,
                    code_id=code_id,
                    menu_name=previous_menu,
                ).pack(),
            )
        )
    kb_builder.row(*btns, width=size)
    return kb_builder.as_markup()


admin_btn = InlineKeyboardButton(
    text="Поддержка📲", url="t.me/+_MbSWnXR3NEwNDcy"
)

async def get_image_and_kb(
    menu_name: str,
    user_id: int,
    next_menu: str | None = None,
    point_id: int | None = None,
    code_id: int | None = None,
    trade_id: int | None = None,
    btns_data: tuple[str, str] | None = None,
    level: int = 0,
    caption: str | None = None,
    previous_menu: str = MAIN_MENU,
    size: tuple[int] = DEFAULT_KEYBOARD_SIZE,
    need_back_btn: bool = True,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """
    Агрегирующая функция создания клавиатуры.
    Возвращаеь изображение с описанием и клавитуру для меню.
    """
    image = await get_img(menu_name=menu_name, caption=caption)
    if menu_name in (DELETE_QR, SEND_QR):
        get_kbs = get_qr_list_kb
    else:
        get_kbs = get_btns
    return (
        image,
        await get_kbs(
            menu_name=menu_name,
            next_menu=next_menu,
            level=level,
            size=size,
            btns_data=btns_data,
            user_id=user_id,
            point_id=point_id,
            trade_id=trade_id,
            code_id=code_id,
            previous_menu=previous_menu,
            need_back_btn=need_back_btn,
        ),
    )
