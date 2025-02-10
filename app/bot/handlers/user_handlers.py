"""Модуль финиш анкеты и обработка кнопок меню самого бота."""

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message

from app.bot.constants import DELETE_CODE, DELETE_ERROR, MAIN_MENU, SUCCESS_DELETE
from app.bot.filters import UserExistFilter

from app.bot.handlers.callbacks.menu_processor import get_menu_content
from app.bot.keyboards.buttons import ADD_QR, MAIN_MENU_PAGES, QR_MENU
from app.bot.keyboards.main_menu_kb import MenuCallBack, get_main_menu_btns
from app.sale_codes.dao import Sale_CodesDAO
from app.users.dao import UsersDAO


user_router = Router()
user_router.message.filter(UserExistFilter())


@user_router.message(CommandStart())
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


@user_router.callback_query(MenuCallBack.filter(F.menu_name.in_(MAIN_MENU_PAGES)))
async def user_menu(
    callback: CallbackQuery,
    callback_data: MenuCallBack,
) -> None:
    """Обработка нажатия кнопок меню."""
    print("основной обработчик")
    await get_menucallback_data(callback, callback_data)
    await callback.answer()
    

async def get_menucallback_data(callback: CallbackQuery, callback_data: MenuCallBack):
    print(callback_data)
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
    return await callback.message.edit_media(
        media=media,
        reply_markup=reply_markup,
    )