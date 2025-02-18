from sqlalchemy import Enum

from app.core.config import settings

CHANGE_POINT = "change_point"
CRITICAL_ERROR = (
    "Критическая ошибка / перезапустите бота\n\n"
    f"Если ошибка повторилась - сообщите админу @{settings.telegram.admin_username}!!"
)

NOTICE = "notice"
CONFIRM = (
    ("YES", "Да"),
    ("NO", "Нет"),
)


DELETE_CODE = "delete_code"
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
QR_SEND = "qr_send"
QR_UPDATE = "qr_update"
REGISTRATION_DONE = (
    "Регистрацияуспешно пройдена! \n"
    "В разделе FAQ вы можете ознакомиться с возможностями бота."
)

REGISTRATION_CONFIRMED, REGISTRATION_CANCELED = dict(CONFIRM).keys()
REGEX_QR_PATTERN = r"(^\d{6,12}_\d{5})"
DELETE_ERROR = "Ошибка удаления."
SUCCESS_DELETE = "✅ QR код УСПЕШНО удален ✅"
SUCCES_DNWLD = "⭐️ Успешная загрузка ⭐️"
DWNLD_ERROR = "⚠️ Ошибка загрузки⚠️"
SUCCES_UPDATE = "⭐️ Код успешно обновлен ✅"
