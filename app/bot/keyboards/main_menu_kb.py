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

from app.core.config import settings
from app.bot.banners import get_img
from app.bot.constants import (
    DEFAULT_KEYBOARD_SIZE,
    MAIN_MENU,
    MAIN_MENU_COMMANDS,
    NO_IMAGE,
)
from app.bot.handlers.callbacks.menucallback import MenuCallBack
from app.bot.keyboards.buttons import BACK_BTN, CHECK_QR, FAQ_QR


KeyboardMarkup: TypeAlias = InlineKeyboardMarkup | ReplyKeyboardMarkup
    
    
async def get_btns(
    *,
    level: int = 0,
    size: tuple[int] = DEFAULT_KEYBOARD_SIZE,
    btns_data: dict[str] | None = None,
    point_id: int | None = None,
    user_id: int | None = None,
    previous_menu: str = MAIN_MENU,
    code_id: int | None = None,
    trade_id: int | None = None
) -> KeyboardMarkup:
    """
    Создание клавиатуры.
    Текст кнопок и колбэк дата берется из констант.
    Если btns_data нет - создается только кнопка Назад.
    """
    keyboard = InlineKeyboardBuilder()
    if btns_data:
        for menu_name, text in btns_data.items():
            keyboard.add(
                InlineKeyboardButton(
                    text=text,
                    callback_data=MenuCallBack(
                        level=level + 1,
                        menu_name=menu_name,
                        user_id=user_id,
                        point_id=point_id,
                        code_id=code_id,
                        trade_id=trade_id
                    ).pack(),
                ),
            )
        if menu_name == FAQ_QR:
            keyboard.add(admin_btn)
    if level > 0:
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


async def set_main_menu(bot: Bot) -> None:
    """Установить основное меню, назначить команды с описаниями."""
    main_menu_commands = [
        BotCommand(command=command, description=description)
        for command, description in MAIN_MENU_COMMANDS.items()
    ]
    await bot.set_chat_menu_button(menu_button=None)
    await bot.set_my_commands(main_menu_commands)
    
admin_btn = InlineKeyboardButton(
            text="Админ", url=f"tg://user?id={settings.telegram.admin_id}"
        )


async def get_image_and_kb(
    menu_name: str,
    user_id: int,
    point_id: int | None = None,
    btns_data: dict[str] | None = None,
    level: int = 0,
    caption: str | None = None,
    previous_menu: str = MAIN_MENU,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """
    Получить изображение, описание и клавитуру для меню.
    Передаются имя меню, описание (опционально) и данные для кнопок.
    """

    try:
        image = await get_img(menu_name=menu_name, caption=caption)
    except Exception:
        image = await get_img(menu_name=NO_IMAGE, caption=caption)
    return (
        image,
        await get_btns(
            btns_data=btns_data, user_id=user_id, level=level, point_id=point_id, previous_menu=previous_menu
        ),
    )
