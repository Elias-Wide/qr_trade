from sqlalchemy import Enum

from app.core.config import settings

CONFIRM = (
    ("YES", "Да"),
    ("NO", "Нет"),
)


class Button:
    MAIN_MENU = "menu"
DELETE_CODE = "delete_code"
DELETE_QR_SIZE: tuple[int] = (1,)
DEFAULT_KEYBOARD_SIZE: tuple[int] = (2,)
FMT_JPG: str = ".jpg"
MAIN_MENU: str = "main_menu"

MAIN_MENU_COMMANDS: dict[str] = {
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
NO_CAPTION = ''
NO_IMAGE: str = "no_image"
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
SUCCESS_DELETE = "✅ QR код УСПЕШНО удален ✅"
# FAQ_MENU = (
#     "Приветствую тебя в qr_trade боте\n"
#     "Бот создан для быстрого обмена qr-кодами между менеджерами "
#     "пунктов выдачи с целью поддержания рейтинга в идеальном состоянии.\n"
#     "Выберите раздел, про который хотите узнать."
# )
#     "Доступно для работы два основных раздела меню: Профиль и Меню QR. \n\n"
#     "ПРОФИЛЬ \n"
#     "В меню профиля ты можешь посмотреть свои личные данные. "
#     "При желании сменить пункт или вовсе его удалит, настроить график работы"
#     "и уведомления. \nМожно включить уведомления по графику, в таком случае, "
#     "Вам будут приходить сообщения о доступных кодах на ваш пункт только в "
#     "те дни, когда вы работаете.\n"
#     "Вы можете и вовсе отключить уведомления, запросить актуальный код можно "
#     "будет через меню QR.\n\n"
#     "QR МЕНЮ \n"
#     "В данном разделе вы можете загрузить/удалить ваши QR коды, а после "
#     "отправить их на целевые пункты.\n"
#     "Кнопка 'Проверить QR' делает запрос и проверяет, есть ли актуальные коды"
#     "на ваш пункт.\n Если у вас назначен рабочий пункт - можно настроить "
#     "уведолмения по графику работы. В таком случае, в тот момент, когда "
#     "кто-то  загружает код для вашего пункта - менеджер, работающий в этот "
#     "день, получает уведомление б этом.\n"
#     "Кнопка 'Отправить QR' - открывает раздел поиска пункта выдачи, можно "
#     "выбрать поиск по адресу или по id пункта\n"
#     "Кнопка 'Удалить QR' - удаление загруженного Вами кода, используйте, "
#     "если загрузили код со старыми данными.\n\n"
#     "P.S. Код писал на коленке, возможны косяки, баги. "
#     "Если есть жалобы, пожелания, благодарности, проклятия - писать админу =)"
# )
