"""Модуль финиш анкеты и обработка кнопок меню самого бота."""

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType, Message
from aiogram.fsm.state import default_state

from app.bot.filters import AdminFilter
from app.bot.handlers.states import AdminStates
from app.bot.utils import read_excel_file


admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(Command("d_points"))
async def procces_dnwld_point_command(message: Message, state: FSMContext):
    """Обработка команды загрузки пунктов."""
    await message.answer(text="Загрузите необходимый файл.")
    await state.set_state(AdminStates.dwnld_points)


@admin_router.message(
    AdminStates.dwnld_points, F.content_type == ContentType.DOCUMENT
)
async def proccess_dwnld_file(message: Message, state: FSMContext):
    """Обработка сообщения, загрузка и обработка файла."""
    await read_excel_file(message=message)
