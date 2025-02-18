"""
Модуль констант для кнопок.
Сначала идут "простые" константы в алфавитном порядке, 
потом сложные - dict, tuple.
"""

from app.bot.constants import MAIN_MENU


ADD_POINT = "add_point"
ADD_QR = "add_qr"
CHECK_QR = "check_qr"
CONFIRM_SALE = "confirm_sale"
BACK_BTN = "Назад ◀️"
DELETE_QR = "del_qr"
DELETE_QR_BTN = "❌QR {} от {}❌"
FAQ_MENU = "faq"
FAQ_QR = "faq_qr"
FAQ_PROFILE = "faq_profile"
QR_SEND = "qr_send"

NOTIFICATIONS = "notifications"
PROFILE = "profile"
QR_MENU = "qr_menu"
SCHEDULE = "schedule"

FAQ_MENU_BTNS = (
    (FAQ_PROFILE, "Профиль"),
    (FAQ_QR, "QR"),
)

MAIN_MENU_BUTTONS = (
    (PROFILE, "Профиль 📋"),
    (FAQ_MENU, "FAQ 📚"),
    (QR_MENU, "QR меню 📨"),
)
MAIN_MENU_PAGES: tuple[str] = (
    MAIN_MENU,
    QR_MENU,
    DELETE_QR,
    FAQ_MENU,
    FAQ_PROFILE,
    FAQ_QR,
    PROFILE,
)
CONFIRM_BTNS = ((CHECK_QR, "✅ Заказ закрыт✅"),)
PROFILE_MENU_BTNS = (
    (ADD_POINT, "Сменить пункт"),
    (NOTIFICATIONS, "Уведомления"),
    (SCHEDULE, "Установить график"),
)

QR_MENU_BTNS = (
    (ADD_QR, "Загрузить код 📨"),
    (QR_SEND, "Отправить код 🚀"),
    (CHECK_QR, "Получить QR 📫"),
    (DELETE_QR, "Удалить код 🗑"),
)

QR_SEND_BTNS = (("by_addres", "Ввести адрес 🖋"), ("by_id", "Ввести id пункта 🔢"))
