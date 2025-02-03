"""
Модуль для работы  изображениями и описаниями сообщений бота.
Содержить функции и константы для выдачи необходимых данных.
"""
from aiogram.types import FSInputFile, InputMediaPhoto

from app.bot.constants import FMT_JPG
from app.core.config import STATIC_DIR


class Captions():
    registration_start = (
        "<b>Привет!  Я - бот обмена QR-кодами между менеджерами 😊</b>\n\n"
        "Давай пройдем простенькую регистрацию для нашей работы."
        "\n😜\n"
        "Вы готовы ответить на несколько вопросов?"
    )

class Images():

    @staticmethod
    async def get_img(menu_name: str, level: int = 0) -> FSInputFile:
        return FSInputFile(STATIC_DIR.joinpath(menu_name + FMT_JPG))