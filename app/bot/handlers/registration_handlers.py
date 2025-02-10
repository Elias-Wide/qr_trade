"""Модуль с функциями анкеты."""

from datetime import timedelta
from typing import Any

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    InlineKeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from app.bot.banners import Captions, get_img
from app.bot.constants import (
    CONFIRM,
    INTRO_SURVEY_TEXT,
    INVALID_DATA_TYPE,
    INVALID_ID_MESSAGE,
    MAIN_MENU,
    MANAGER_ID,
    POINT_ID,
    REGISTRATION_CANCELED,
    REGISTRATION_CONFIRMED,
    REGISTRATION_DONE,
    SurveyQuestions,
)
from app.bot.filters import (
    AccesCodeFilter,
    ManagerExistFilter,
    PointExistFilter,
    UserExistFilter,
)
from app.bot.handlers.user_handlers import process_start_command
from app.bot.keyboards.registration_kb import (
    create_back_to_menu_kb,
    create_registration_kb,
)
from app.users.dao import UsersDAO

from app.bot.handlers.states import RegistrationStates


registration_router = Router()


async def return_to_main_menu(
    message: Message,
    state: FSMContext,
) -> None:
    """Возврат в главное меню."""
    await state.set_state(RegistrationStates.finished)
    await process_start_command(message, state)


@registration_router.message(default_state, CommandStart(), ~UserExistFilter())
async def begin_registration(
    message: Message,
    state: FSMContext,
) -> None:
    """Приветствие и согласие ответить на вопросы."""
    await state.update_data(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
    )
    await message.answer_photo(
        photo=await get_img("registration_start"),
        caption=Captions.registration_start,
        reply_markup=await create_registration_kb(),
    )
    await state.set_state(RegistrationStates.consent_confirm)


@registration_router.callback_query(F.data == REGISTRATION_CANCELED)
async def handle_survey_cancel(
    callback_query: CallbackQuery,
    state: FSMContext,
) -> None:
    """Отказ от регистрации."""
    await state.set_state(default_state)
    await callback_query.message.answer_photo(
        photo=await get_img("no_registr"),
        caption=Captions.no_registr,
    )


@registration_router.callback_query(
    RegistrationStates.consent_confirm, F.data == REGISTRATION_CONFIRMED
)
async def ask_access_code(
    callback_query: CallbackQuery,
    state: FSMContext,
) -> None:
    """Запрос кода доступа к боту."""
    await callback_query.message.answer(text=SurveyQuestions.ACCESS_CODE)
    await state.set_state(RegistrationStates.access_code)


@registration_router.message(
    RegistrationStates.access_code, F.content_type == "text", AccesCodeFilter()
)
async def ask_manager_id(
    message: Message,
    state: FSMContext,
) -> None:
    """Вопрос про manager id, после согласия анкетироваться."""
    await message.answer(text=SurveyQuestions.MANAGER_ID)
    await state.set_state(RegistrationStates.manager_id_question)


@registration_router.message(
    RegistrationStates.manager_id_question,
    F.text.isdigit(),
    ManagerExistFilter(),
)
async def ask_point_id(message: Message, state: FSMContext) -> None:
    """Сохранение client id в state. Вопрос про point id."""
    await state.update_data(manager_id=int(message.text))
    await message.answer(text=SurveyQuestions.POINT_ID)
    await state.set_state(RegistrationStates.point_id_question)


@registration_router.message(
    RegistrationStates.point_id_question, F.text.isdigit(), PointExistFilter()
)
async def finish_registration(
    message: Message,
    state: FSMContext,
) -> None:
    """
    Сохранение point в state.

    Запись инфо из state в БД. Завершение регистрации.
    Создание модели пользователя по полученным данным.
    """
    await state.update_data(
        point_id=int(message.text),
    )
    registration_data = await state.get_data()
    await UsersDAO.create(registration_data),
    await message.answer_photo(await get_img(menu_name="registration_done"))

    await state.set_state(RegistrationStates.finished)
    await process_start_command(message, state)


@registration_router.message(RegistrationStates.manager_id_question, ~F.text.isdigit())
@registration_router.message(RegistrationStates.point_id_question, ~F.text.isdigit())
async def handle_ivalid_data_type(message: Message):
    """
    Сообщение о невалидном типе введенных данных.
    При обработке point или manager id пользователь
    должен отправить только цифры, иначе срабатывает данный хэндлер."""
    await send_ivalid_data_type_message(message)


@registration_router.message(
    RegistrationStates.access_code, F.content_type == "text", ~AccesCodeFilter()
)
async def handle_invalid_acces_code(message: Message) -> None:
    """Сообщение о введенном невалидном manager id."""
    await message.answer(text="🔴Неверный код доступа🔴")


@registration_router.message(RegistrationStates.access_code)
async def handle_invalid_acces_code_type(message: Message):
    """Сообщение а невалидном типе данных при обработке кода доступа."""
    await send_ivalid_data_type_message(message)


@registration_router.message(
    RegistrationStates.manager_id_question, F.text.isdigit(), ~ManagerExistFilter()
)
async def handle_invalid_manager_id(message: Message) -> None:
    """Сообщение о введенном невалидном manager id."""
    await send_ivalid_data_type_message(data_type=MANAGER_ID, message=message)


@registration_router.message(
    RegistrationStates.point_id_question, F.text.isdigit(), ~PointExistFilter()
)
async def handle_invalid_point_id(message: Message) -> None:
    """Сообщение о введенном невалидном point id."""
    await send_ivalid_data_type_message(data_type=POINT_ID, message=message)


async def send_ivalid_data_type_message(message: Message, data_type: str = None):
    if not data_type:
        text = INVALID_DATA_TYPE
    else:
        text = INVALID_ID_MESSAGE[data_type]
    await message.answer(text=text)


@registration_router.message(CommandStart(), UserExistFilter())
async def handle_existing_user(
    message: Message,
    state: FSMContext,
) -> None:
    """Сообщение о уже существующем пользователе."""
    await state.set_state(RegistrationStates.finished)
    await return_to_main_menu(message, state)
