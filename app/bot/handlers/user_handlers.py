"""Модуль финиш анкеты и обработка кнопок меню самого бота."""

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message
from aiogram.utils.chat_action import ChatActionSender

from app.bot.constants import MAIN_MENU
from app.bot.filters import UserExistFilter

# from app.bot.handlers.menu_processor import get_menu_content
from app.bot.handlers.callbacks.menu_processor import get_menu_content
from app.bot.handlers.states import RegistrationStates
from app.bot.keyboards.main_menu_kb import MenuCallBack, get_main_menu_btns
from app.bot.banners import captions
from app.users.dao import UsersDAO


menu_router = Router()
menu_router.message.filter(UserExistFilter())


@menu_router.message(CommandStart())
async def process_start_command(
    message: Message,
    state: FSMContext,
) -> None:
    """После завершения анкетирования. Начало самого бота."""
    user = await UsersDAO.get_by_attribute(
        attr_name="telegram_id", attr_value=message.from_user.id
    )
    media, reply_markup = await get_menu_content(
        level=0,
        menu_name=MAIN_MENU,
        user_id=user.id,
    )
    await message.answer_photo(
        photo=media.media,
        caption=media.caption,
        reply_markup=reply_markup,
    )
    await state.clear()


@menu_router.callback_query(MenuCallBack.filter())
async def user_menu(
    callback: CallbackQuery,
    callback_data: MenuCallBack,
) -> None:
    """Обработка нажатия кнопок меню."""
    if not callback_data.user_id:
        user = await UsersDAO.get_by_attribute(
            attr_name="telegram_id", attr_value=callback.message.from_user.id
        )
        callback_data.user_id = user.id
    media, reply_markup = await get_menu_content(
        level=callback_data.level,
        menu_name=callback_data.menu_name,
        user_id=callback_data.user_id,
    )
    await callback.message.edit_media(
        media=media,
        reply_markup=reply_markup,
    )
    await callback.answer()
