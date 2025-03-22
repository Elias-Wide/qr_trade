"""Модуль финиш анкеты и обработка кнопок меню самого бота."""

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType, Message
from aiogram.fsm.state import default_state

from app.bot.scheduler import send_order_notification
from app.core.logging import logger
from app.bot.filters import AdminFilter
from app.bot.handlers.states import AdminStates
from app.bot.utils import read_excel_file
from app.points.dao import PointsDAO


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
    point_list = await read_excel_file(message=message)
    for point_data in point_list:
        await PointsDAO.create(point_data)
    await message.answer(text="Success!")


@admin_router.message(Command("u_points"))
async def procces_updt_point_command(message: Message, state: FSMContext):
    """Обработка команды загрузки пунктов."""
    await message.answer(text="Загрузите необходимый файл для обновления.")
    await state.set_state(AdminStates.updt_points)


@admin_router.message(
    AdminStates.updt_points, F.content_type == ContentType.DOCUMENT
)
async def proccess_dwnld_updt_file(message: Message, state: FSMContext):
    """Обработка сообщения, загрузка и обработка файла."""
    try:
        point_list = await read_excel_file(message=message)
        for point_data in point_list:
            point = await PointsDAO.get_by_attribute(
                attr_name="point_id", attr_value=point_data["point_id"]
            )
            await PointsDAO.update(point, point_data)
        await message.answer(text="Данные успешно обновлены!")
    except Exception as error:
        logger(error)


@admin_router.message(Command("test_msg"))
async def process_check_command(
    message: Message,
) -> None:
    """Обработка нажатия кнопки open_qr."""
    logger()
    try:
        await send_order_notification()
    except Exception as error:
        logger(error)
