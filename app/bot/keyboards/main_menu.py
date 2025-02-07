from typing import TypeAlias

from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.constants import DEFAULT_KEYBOARD_SIZE, MAIN_MENU_COMMANDS
from app.bot.keyboards.buttons import MAIN_MENU_BUTTONS, PROFILE

KeyboardMarkup: TypeAlias = InlineKeyboardMarkup | ReplyKeyboardMarkup


class MenuCallBack(CallbackData, prefix="menu"):
    """
    Фабрика колбэков.

    level :: атрибут указывающий на глубину(шаг) меню.

    menu_name :: название меню.
    """

    level: int
    menu_name: str
    tg_user_id: int | None = None
    manager_id: int = 1
    ok: str | None = None
    yes_no: str | None = None


async def get_main_menu_btns(
    *,
    level: int,
    sizes: tuple[int] = DEFAULT_KEYBOARD_SIZE,
) -> KeyboardMarkup:
    """Получить кнопки для главного меню."""
    keyboard = InlineKeyboardBuilder()
    for menu_name, text in MAIN_MENU_BUTTONS.items():
        keyboard.add(
            InlineKeyboardButton(
                text=text,
                callback_data=MenuCallBack(
                    level=level,
                    menu_name=menu_name,
                ).pack(),
            ),
        )
        # else:
        #     keyboard.add(
        #         InlineKeyboardButton(
        #             text=text,
        #             callback_data=MenuCallBack(
        #                 level=level,
        #                 menu_name=menu_name,
        #             ).pack(),
        #         ),
        #     )
    return keyboard.adjust(*sizes).as_markup()


async def set_main_menu(bot: Bot) -> None:
    """Установить основное меню, назначить команды с описаниями."""
    main_menu_commands = [
        BotCommand(command=command, description=description)
        for command, description in MAIN_MENU_COMMANDS.items()
    ]
    await bot.set_chat_menu_button(menu_button=None)
    await bot.set_my_commands(main_menu_commands)
