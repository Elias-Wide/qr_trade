"""Модуль главного и других меню."""

from aiogram.types import CallbackQuery, Message

from app.core.constants import CRITICAL_ERROR, MAIN_MENU
from app.bot.handlers.callbacks.menu_processor import get_menu_content
from app.bot.handlers.callbacks.menucallback import MenuCallBack
from app.users.dao import UsersDAO
from app.core.logging import logger


async def procces_main_menu_comand(
    message: Message, level: int = 0, menu_name: str = MAIN_MENU
) -> None:
    """Получить данные пользователя из сообщения и открыть меню."""
    try:
        user = await UsersDAO.get_by_attribute(
            attr_name="telegram_id", attr_value=message.from_user.id
        )

        media, reply_markup = await get_menu_content(
            level=level, menu_name=menu_name, user_id=user.id
        )
        await message.answer_photo(
            photo=media.media,
            caption=media.caption,
            reply_markup=reply_markup,
        )
    except Exception as error:
        logger(error)
        await message.answer(text=CRITICAL_ERROR)


async def get_menucallback_data(
    callback: CallbackQuery, callback_data: MenuCallBack
) -> None:
    """Получить колбэк дата"""
    if not callback_data.user_id:
        user = await UsersDAO.get_by_attribute(
            attr_name="telegram_id", attr_value=callback.message.chat.id
        )
        callback_data.user_id = user.id
    logger()
    media, reply_markup = await get_menu_content(
        level=callback_data.level,
        menu_name=callback_data.menu_name,
        user_id=callback_data.user_id,
        point_id=callback_data.point_id,
        trade_id=callback_data.trade_id,
        code_id=callback_data.code_id,
    )
    await callback.message.edit_media(
        media=media,
        reply_markup=reply_markup,
    )
