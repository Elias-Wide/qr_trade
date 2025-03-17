# from typing import TypeAlias

# from aiogram.filters.callback_data import CallbackData
# from aiogram.types import (
#     BotCommand,
#     InlineKeyboardButton,
#     InlineKeyboardMarkup,
#     InputMediaPhoto,
#     ReplyKeyboardMarkup,
# )
# from aiogram import Bot
# from aiogram.utils.keyboard import InlineKeyboardBuilder

# from app.bot.keyboards.banners import get_img
# from app.bot.constants import (
#     DEFAULT_KEYBOARD_SIZE,
#     MAIN_MENU,
# )
# from app.bot.handlers.callbacks.menucallback import MenuCallBack
# from app.bot.keyboards.buttons import (
#     BACK_BTN,
#     FAQ_MENU,
#     FAQ_MENU_BTNS,
#     MAIN_MENU_BUTTONS,
#     PROFILE,
#     QR_MENU,
# )
# from app.core.config import settings
# from app.users.models import Users

# KeyboardMarkup: TypeAlias = InlineKeyboardMarkup | ReplyKeyboardMarkup


# async def get_faq_kb(
#     level: int,
#     user_id: int,
#     size: tuple[int] = DEFAULT_KEYBOARD_SIZE,
# ) -> KeyboardMarkup:
#     """
#     Получить клавиутуру для раздела FAQ.
#     """
#     keyboard = InlineKeyboardBuilder()
#     for callback_data, text in FAQ_MENU_BTNS.items():
#         keyboard.add(
#             InlineKeyboardButton(
#                 text=text,
#                 callback_data=MenuCallBack(
#                     menu_name=callback_data,
#                     level=level + 1,
#                     user_id=user_id,
#                 ).pack(),
#             ),
#         )
#     keyboard.add(
#         InlineKeyboardButton(
#             text="Админ", url=f"tg://user?id={settings.telegram.admin_id}"
#         ),
#     )
#     keyboard.add(
#         InlineKeyboardButton(
#             text=BACK_BTN,
#             callback_data=MenuCallBack(
#                 user_id=user_id,
#                 level=level,
#                 menu_name=MAIN_MENU,
#             ).pack(),
#         )
#     )
#     return keyboard.adjust(*size).as_markup()


# async def get_faq_side_menu_kb(
#     level: int, user_id: int, size: tuple[int] = DEFAULT_KEYBOARD_SIZE
# ) -> KeyboardMarkup:
#     keyboard = InlineKeyboardBuilder()
#     keyboard.add(
#         InlineKeyboardButton(
#             text=BACK_BTN,
#             callback_data=MenuCallBack(
#                 user_id=user_id,
#                 level=level - 1,
#                 menu_name=FAQ_MENU,
#             ).pack(),
#         )
#     )
#     return keyboard.adjust(*size).as_markup()
