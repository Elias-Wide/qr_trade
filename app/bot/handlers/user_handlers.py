"""Модуль финиш анкеты и обработка кнопок меню самого бота."""

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.bot.constants import MAIN_MENU
from app.bot.filters import UserExistFilter

from app.bot.handlers.callbacks.menu_processor import get_menu_content
from app.bot.keyboards.buttons import MAIN_MENU_PAGES
from app.bot.keyboards.main_menu_kb import MenuCallBack
from app.users.dao import UsersDAO
from app.core.logging import get_logger

logger = get_logger(__name__)
user_router = Router()
user_router.message.filter(UserExistFilter())


@user_router.message(CommandStart())
async def process_start_command(
    message: Message,
    state: FSMContext,
) -> None:
    logger.info
    """После завершения анкетирования. Начало самого бота."""
    user = await UsersDAO.get_by_attribute(
        attr_name="telegram_id", attr_value=message.from_user.id
    )

    media, reply_markup = await get_menu_content(
        level=0, menu_name=MAIN_MENU, user_id=user.id, point_id=user.point_id
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
    try:
        
        if not all((callback_data.user_id, callback_data.point_id)):
            user = await UsersDAO.get_by_attribute(
                attr_name="telegram_id", attr_value=callback.message.chat.id
            )
            callback_data.user_id = user.id
            callback_data.point_id = user.point_id
        await get_menucallback_data(callback, callback_data)
        await callback.answer()
    except:
        await callback.answer(text="Критическая ошибка / перезапустите бота", show_alert=True)


async def get_menucallback_data(callback: CallbackQuery, callback_data: MenuCallBack):
    print(callback_data)
    media, reply_markup = await get_menu_content(
        level=callback_data.level,
        menu_name=callback_data.menu_name,
        user_id=callback_data.user_id,
        point_id=callback_data.point_id,
    )
    return await callback.message.edit_media(
        media=media,
        reply_markup=reply_markup,
    )
