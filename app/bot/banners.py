"""
Модуль для работы  изображениями и описаниями сообщений бота.
Содержить функции и константы для выдачи необходимых данных.
"""

from aiogram.types import FSInputFile, InputMediaPhoto

from app.bot.constants import FMT_JPG
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
    main_menu = ()


class Images:

    @staticmethod
    async def get_img(menu_name: str, level: int = 0) -> FSInputFile:
        return FSInputFile(BANNERS_DIR.joinpath(menu_name + FMT_JPG))
