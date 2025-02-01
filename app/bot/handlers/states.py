"""Модуль содержащий состояния анкеты."""

from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    """Класс описывающий состояния анкеты."""

    consent_confirm = State()
    manager_id_question = State()
    client_id_question = State()
    point_id_question = State()
    finished = State()
