"""
Модуль констант для текста и колбэкдата кнопок.
Сначала идут "простые" константы в алфавитном порядке, 
потом сложные - dict, tuple.
"""

from app.core.constants import MAIN_MENU, NOTIFICATION_TYPE


ADD_POINT: str = "add_point"
ADD_QR: str = "add_qr"
BACK_BTN: str = "Назад ◀️"
CANCEL: str = "cancel"
CANCEL_SEARCH: str = "Отменить поиск"
CHANGE_POINT = "change_point"
CHECK_QR: str = "check_qr"
CONFIRM_SALE: str = "confirm_sale"
CONFIRM_SCHEDULE: str = "confirm_schedule"
CONFIRM_SEND: str = "confirm_send"
DELETE_QR: str = "del_qr"
DELETE_QR_BTN = "QR{} ❌"
EMPTY_BTN: str = "Это пустые кнопки, не балуйся!"
FAQ_MENU: str = "faq"
FAQ_PROFILE: str = "faq_profile"
FAQ_QR: str = "faq_qr"
MAX_POINTS_LIST_MSG: str = (
    "Вы добавили максимальное количество пунктов! \n"
    "Подтвердите отправку. \n\n"
)
NONE_MENU = "none"
NOTIFICATIONS: str = "notifications"
POINT_SEARCH: str = "point_search"
PROFILE: str = "profile"
QR_INFO_BTN: str = "QR{} ✳️"
QR_MENU: str = "qr_menu"
SET_SCHEDULE: str = "set_schedule"
SEND_QR: str = "qr_send"
SCHEDULE: str = "schedule"
UPDATE_QR: str = "qr_update"

CONFIRM_SCHEDULE_BTN: tuple[str] = (CONFIRM_SCHEDULE, "Сохранить график 📝")
CONFIRM_SEND_BTNS: tuple[tuple[str]] = ((CONFIRM_SEND, "📦 Отправить 📦"),)
CONFIRM_BTNS: tuple[tuple[str]] = ((CHECK_QR, "✅ Заказ закрыт✅"),)
CALENDAR_BTNS: tuple[tuple[str]] = tuple(
    (NONE_MENU, text) for text in ("ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС")
)


FAQ_MENU_BTNS: tuple[tuple[str]] = (
    (FAQ_PROFILE, "Профиль"),
    (FAQ_QR, "QR"),
)
NOTIFICATIONS_BTNS = NOTIFICATION_TYPE
MAIN_MENU_BUTTONS: tuple[tuple[str]] = (
    (PROFILE, "Профиль 📋"),
    (FAQ_MENU, "FAQ 📚"),
    (QR_MENU, "QR меню 📨"),
)
MAIN_MENU_PAGES: tuple[str] = (
    MAIN_MENU,
    QR_MENU,
    DELETE_QR,
    SEND_QR,
    FAQ_MENU,
    FAQ_PROFILE,
    FAQ_QR,
    PROFILE,
    NOTIFICATIONS,
)
PROFILE_MENU_BTNS: tuple[tuple[str]] = (
    (CHANGE_POINT, "Сменить пункт 🛍"),
    (NOTIFICATIONS, "🔊Уведомления🔇"),
    (SCHEDULE, "График работы 🗓"),
)

QR_MENU_BTNS: tuple[tuple[str]] = (
    (ADD_QR, "Загрузить код 📨"),
    (SEND_QR, "Отправить код 🚀"),
    (CHECK_QR, "Получить QR 📫"),
    (DELETE_QR, "Удалить код 🗑"),
)

QR_SEND_BTNS: tuple[tuple[str]] = (
    ("by_addres", "Ввести адрес 🖋"),
    ("by_id", "Ввести id пункта 🔢"),
)

QR_BTN_TYPE: dict[str] = {DELETE_QR: DELETE_QR_BTN, SEND_QR: QR_INFO_BTN}
