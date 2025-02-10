"""
Модуль для работы  изображениями и описаниями сообщений бота.
Содержить функции и константы для выдачи необходимых данных.
"""

import os

from aiogram.types import FSInputFile, InputMediaPhoto

from app.bot.constants import FAQ_DESCRIPTION, FMT_JPG, NO_IMAGE
from app.core.config import STATIC_DIR

BANNERS_DIR = STATIC_DIR / "banners"


class Captions:
    registration_start = (
        "<b>Привет!  Я - бот обмена QR-кодами между менеджерами 😊</b>\n\n"
        "Давай пройдем простенькую регистрацию для нашей работы."
        "\n😜\n"
        "Вы готовы ответить на несколько вопросов?"
    )
    registration_done = (
        "Регистрация успешно пройдена! \n\n"
        "В разделе FAQ вы можете ознакомиться с возможностями бота."
    )
    main_menu = ""
    no_image = "no caption"
    no_registr = "Жаль, возвращайся, когда передумаешь."
    no_qr_today = "Нет загруженных QR кодов на сегодня. \n"
    qr_today = "На сегодня загружено QR кодов: {f_qr} "
    qr_menu = "На сегодня загружено QR кодов: {f_qr} "
    faq = "FAQ_DESCRIPTION"


async def get_img(
    menu_name: str, level: int = 0, caption: str = None
) -> InputMediaPhoto:
    """
    Получить изображение.
    В функцию передаются имя меню, уровень меню и описание,
    если описания нет, то оно берется из класса Captions.
    Если нет необходимого изображения, то берется картинка 'no_image'.
    """
    if caption is None:
        caption = getattr(captions, menu_name)
    if not await is_file_in_dir(f"{menu_name}.jpg", BANNERS_DIR):
        menu_name = NO_IMAGE
    image = FSInputFile(BANNERS_DIR.joinpath(menu_name + FMT_JPG))
    return InputMediaPhoto(media=image, caption=caption)


async def is_file_in_dir(name, path):
    """Проверить, если ли необходимое изображение в директории."""
    for root, dirs, files in os.walk(path):
        if name in files:
            return True
        return False


captions = Captions()
