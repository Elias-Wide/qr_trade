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
    MAIN_MENU,
    MAIN_MENU_COMMANDS,
    NO_IMAGE,
)
from app.bot.handlers.callbacks.menucallback import MenuCallBack
from app.bot.keyboards.buttons import BACK_BTN, FAQ_MENU, FAQ_MENU_BTNS, MAIN_MENU_BUTTONS, PROFILE
from app.core.config import settings
from app.users.models import Users

KeyboardMarkup: TypeAlias = InlineKeyboardMarkup | ReplyKeyboardMarkup


async def get_main_menu_btns(
    *, level: int, sizes: tuple[int] = DEFAULT_KEYBOARD_SIZE, user_id: int | None = None
) -> KeyboardMarkup:
    """Получить кнопки для главного меню."""
    keyboard = InlineKeyboardBuilder()
    for menu_name, text in MAIN_MENU_BUTTONS.items():
        keyboard.add(
            InlineKeyboardButton(
                text=text,
                callback_data=MenuCallBack(
                    user_id=user_id,
                    level=level,
                    menu_name=menu_name,
                ).pack(),
            ),
        )
    return keyboard.adjust(*sizes).as_markup()


async def set_main_menu(bot: Bot) -> None:
    """Установить основное меню, назначить команды с описаниями."""
    main_menu_commands = [
        BotCommand(command=command, description=description)
        for command, description in MAIN_MENU_COMMANDS.items()
    ]
    await bot.set_chat_menu_button(menu_button=None)
    await bot.set_my_commands(main_menu_commands)


async def get_side_menu_btns(
    *,
    level: int = 0,
    size: tuple[int] = DEFAULT_KEYBOARD_SIZE,
    btns_data: dict[str],
    user_id: int | None = None,
) -> KeyboardMarkup:
    """Создание клавиатуры для дополнительных меню."""
    keyboard = InlineKeyboardBuilder()
    for menu_name, text in btns_data.items():
        keyboard.add(
            InlineKeyboardButton(
                text=text,
                callback_data=MenuCallBack(
                    level=level + 1,
                    menu_name=menu_name,
                    user_id=user_id,
                ).pack(),
            ),
        )
    keyboard.add(
        InlineKeyboardButton(
            text=BACK_BTN,
            callback_data=MenuCallBack(
                user_id=user_id,
                level=level,
                menu_name=MAIN_MENU,
            ).pack(),
        )
    )
    return keyboard.adjust(*size).as_markup()


async def get_image_and_kb(
    menu_name: str, user_id: int, btns_data: dict[str], caption: str = None
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """
    Получить изображение, описание и клавитуру для меню.
    Передаются имя меню, описание (опционально) и данные для кнопок.
    """

    try:
        image = await get_img(menu_name=menu_name, caption=caption)
    except Exception:
        image = await get_img(menu_name=NO_IMAGE, caption=caption)
    return (image, await get_side_menu_btns(btns_data=btns_data, user_id=user_id))


