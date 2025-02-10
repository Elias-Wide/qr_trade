"""
Модуль констант для кнопок.
Сначала идут "простые" константы в алфавитном порядке, 
потом сложные - dict, tuple.
"""

ADD_POINT = "add_point"
ADD_QR = "add_qr"
CHECK_QR = "check_qr"
BACK_BTN = "Назад ◀️"
DELETE_QR = "del_qr"
FAQ_MENU = "faq"
FAQ_QR = "faq_qr"
FAQ_PROFILE = "faq_profile"


NOTIFICATIONS = "notifications"
PROFILE = "profile"
QR_MENU = "qr_menu"
SCHEDULE = "schedule"

FAQ_MENU_BTNS = {
    FAQ_PROFILE: "Профиль",
    FAQ_QR: "QR",
}

MAIN_MENU_BUTTONS = {
    PROFILE: "Профиль 📋",
    FAQ_MENU: "FAQ 📚",
    QR_MENU: "QR меню 📨",
}

PROFILE_MENU_BTNS = {
    ADD_POINT: "Сменить пункт",
    NOTIFICATIONS: "Уведомления",
    SCHEDULE: "Установить график",
}

QR_MENU_BTNS = {
    ADD_QR: "Загрузить код 📨",
    CHECK_QR: "Проверить наличие QR на мой пункт",
    DELETE_QR: "Удалить код 🗑",
}
