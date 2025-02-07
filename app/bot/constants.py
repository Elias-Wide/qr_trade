from sqlalchemy import Enum

from app.core.config import settings

CONFIRM = (
    ("YES", "Да"),
    ("NO", "Нет"),
)


class Button:
    MAIN_MENU = "menu"


DEFAULT_KEYBOARD_SIZE = (2,)
FMT_JPG = ".jpg"
MAIN_MENU = "main_menu"

MAIN_MENU_COMMANDS = {
    "/start": "Перезапуск бота",
    "/help": "Справка",
}


class SurveyQuestions(str, Enum):
    """Перечисление вопросов анкеты регистрации."""

    CONSENT = "Вы готовы ответить на несколько вопросов?"
    ACCESS_CODE = "Введите код для регистрации 🔒"
    MANAGER_ID = "Введите Ваш рабочий (manager) ID"
    CLIENT_ID = (
        "Введите ваш ID клиента\n"
        "P.S. Вы можете его найти, отсканировав свой qr "
        "в пользовательском приложении. После сканирования "
        "вы получите два набора цифр, разделенных нижним "
        "подчеркиванием (например, 57348732_12345).\n"
        "Первый набор цифр - это Ваш ID"
        "\n😜\n"
    )
    POINT_ID = (
        "Введите ID вашего пункта.\n"
        "Он необходим для получения уведомлений. "
        "Если нет постоянного пункта, но вы помогаете другим с рейтингом - "
        "напишите 1."
    )


INTRO_SURVEY_TEXT = (
    "<b>Привет! Я - бот обмена QR-кодами между менеджерами=)</b>\n"
    "Давай пройдем простенькую регистрацию для нашей работы."
    "\n😜\n"
)
MANAGER_ID, POINT_ID = "manager_id", "point_id"

INVALID_DATA_TYPE = "Неверный формат введенных данных!"
INVALID_ID_MESSAGE = {
    MANAGER_ID: (
        "Введенный id менеджера уже кем-то занят.\n"
        "Если вы сменили телеграмм аккаунт - обратитесь "
        "в поддержку."
    ),
    POINT_ID: (
        f"Пункт с данным id отсутствует в бд. \n\n"
        f"Обратитесь к админу @{settings.telegram.admin_username}"
    ),
}

REGISTRATION_DONE = (
    "Регистрацияуспешно пройдена! \n"
    "В разделе FAQ вы можете ознакомиться с возможностями бота."
)

REGISTRATION_CONFIRMED, REGISTRATION_CANCELED = dict(CONFIRM).keys()
