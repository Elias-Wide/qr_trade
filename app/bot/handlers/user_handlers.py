"""Модуль финиш анкеты и обработка кнопок меню самого бота."""

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaVideo, Message
from aiogram.utils.chat_action import ChatActionSender
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.banners import Images
from app.bot.constants import MAIN_MENU
from app.bot.filters import UserExistFilter

# from app.bot.handlers.menu_processor import get_menu_content
from app.bot.handlers.states import RegistrationStates
from app.bot.keyboards.main_menu import MenuCallBack, get_main_menu_btns
from app.users.dao import UsersDAO


main_router = Router()
main_router.message.filter(UserExistFilter())


@main_router.message(CommandStart())
async def process_start_command(
    message: Message,
    state: FSMContext,
) -> None:
    """После завершения анкетирования. Начало самого бота."""
    user = await UsersDAO.get_by_attribute("telegram_id", message.chat.id)

    # media, reply_markup = awaitawait get_menu_content(
    #     level=0,
    #     menu_name=MAIN_MENU,
    #     user=user
    # )
    await message.answer_photo(
        photo=await Images.get_img(menu_name=MAIN_MENU),
        caption="MAIN MENU",
        reply_markup=await get_main_menu_btns(level=0),
    )
    await state.clear()


@main_router.callback_query(MenuCallBack.filter())
async def user_menu(
    callback: CallbackQuery,
    callback_data: MenuCallBack,
    session: AsyncSession,
) -> None:
    """Обработка нажатия кнопок меню."""
    user = await UsersDAO.get_by_attribute(
        "telegram_id",
        callback.from_user.id,
    )
    media, reply_markup = await get_menu_content(
        session=session,
        level=callback_data.level,
        menu_name=callback_data.menu_name,
        user=user,
    )
    await callback.message.edit_media(
        media=media,
        reply_markup=reply_markup,
    )
    await callback.answer()
