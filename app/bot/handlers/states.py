"""Модуль содержащий состояния анкеты."""

from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    """Класс описывающий состояния анкеты."""

    consent_confirm = State()
    access_code = State()
    manager_id_question = State()
    point_id_question = State()
    finished = State()


class MenuQRStates(StatesGroup):
    """Класс состояний меню qr-кодов."""

    add_qr = State()
    point_search = State()


class ProfileStates(StatesGroup):
    """Класс состояний меню профиля."""

    change_point = State()
    schedule = State()


class AdminStates(StatesGroup):
    """Класс состояний для команд админа."""

    dwnld_points = State()
    updt_points = State()
