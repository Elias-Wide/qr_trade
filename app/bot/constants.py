from sqlalchemy import Enum

from app.core.config import settings

CRITICAL_ERROR = (
    "Критическая ошибка / перезапустите бота\n\n"
    f"Если ошибка повторилась - сообщите админу @{settings.telegram.admin_username}!!"
)

NOTICE = "notice"
CONFIRM = (
    ("YES", "Да"),
    ("NO", "Нет"),
)

DELETED = "deleted"
DELETE_CODE = "delete_code"
POINT_LIST_KB_SIZE: int = 1
DEFAULT_KEYBOARD_SIZE: int = 2
FMT_GIF: str = ".gif"
FMT_JPG: str = ".jpg"
SEARCH_GIFS: tuple[str] = tuple(f"search_{n}" for n in range(5))
MAIN_MENU: str = "main_menu"
OPEN_QR = "open_qr"
MAIN_MENU_COMMANDS: dict[str] = {
    "/start": "Перезапуск бота/открыть меню",
    "/open_qr": "Открыть раздел QR",
}
MONTH = {
    1: "янв",
    2: "фев",
    3: "мар",
    4: "апр",
    5: "мая",
    6: "июн",
    7: "июл",
    8: "авг",
    9: "сен",
    10: "окт",
    11: "ноя",
    12: "дек",
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
NEXT_QR = "Успешно ✅ Держи следующий QR 🧤"
NO_CAPTION = ""
NO_IMAGE: str = "no_image"
NOT_FOUND = "not_found"
NOTIFICATION_TYPE = (
    ("off", "🔕 ВЫКЛ 🔕"), ("always", "🔊 ВКЛ 🔊"), ("by_schedule", "По графику 🗓")
)
INVALID_DATA_TYPE: str = "Неверный формат введенных данных!"
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
REGEX_QR_PATTERN = r"(^\d{6,12}_\d{5})"
DELETE_ERROR = "Ошибка удаления."
DWNLD_ERROR = "⚠️ Ошибка загрузки⚠️"
SUCCESS_DELETE = "✅ QR код УСПЕШНО удален ✅"
SUCCES_DNWLD = "⭐️ Код {} успешно загружен⭐️"
SUCCES_UPDATE = "⭐️ Код {} успешно обновлен ✅"
TYPE_POINT = "Введите ID вашего пункта"