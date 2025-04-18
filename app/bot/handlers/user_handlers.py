"""Модуль финиш анкеты и обработка кнопок меню самого бота."""

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.core.constants import OPEN_QR

from app.bot.handlers.callbacks.main_menu import (
    get_menucallback_data,
    procces_main_menu_comand,
)
from app.bot.keyboards.buttons import MAIN_MENU_PAGES, QR_MENU
from app.bot.keyboards.main_kb_builder import MenuCallBack
from app.core.logging import logger


user_router = Router()


@user_router.message(CommandStart())
async def process_start_command(
    message: Message,
    state: FSMContext,
) -> None:
    """После завершения анкетирования. Начало самого бота."""
    logger()
    await procces_main_menu_comand(message)
    await state.clear()


@user_router.message(Command(OPEN_QR))
async def process_open_qr_command(
    message: Message,
    state: FSMContext,
) -> None:
    """Обработка нажатия кнопки open_qr."""
    logger()
    await procces_main_menu_comand(message, level=1, menu_name=QR_MENU)
    await state.clear()


@user_router.callback_query(
    MenuCallBack.filter(F.menu_name.in_(MAIN_MENU_PAGES))
)
async def user_menu(
    callback: CallbackQuery, callback_data: MenuCallBack, state: FSMContext
) -> None:
    """Обработка нажатия кнопок меню."""
    await state.clear()
    try:
        await get_menucallback_data(callback, callback_data)
        await callback.answer()
    except Exception as error:
        logger(error)
        await callback.answer(
            text="Критическая ошибка / перезапустите бота", show_alert=True
        )
