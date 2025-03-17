from datetime import datetime
import os
import qrtools
import re
import random
import string
from io import BytesIO
from PIL import Image
from pyzbar.pyzbar import decode
from PIL import Image
from aiogram.types import ContentType, Message
import openpyxl
import segno
from app.core.constants import (
    FMT_JPG,
    MONTH,
    NOTIFICATION_TYPE,
    REGEX_QR_PATTERN,
)
from app.bot.create_bot import bot
from app.bot.keyboards.buttons import NOTIFICATIONS_BTNS
from app.core.config import QR_DIR
from app.core.logging import logger
from app.core.utils import encode_data
from app.sale_codes.dao import Sale_CodesDAO
from app.schedules.dao import SchedulesDAO
from app.points.models import Points
from app.users.dao import UsersDAO


async def generate_filename() -> str:
    """Генерирует рандомное имя для файла."""
    filename = [
        random.choice(
            string.ascii_lowercase + string.digits
            if i != 5
            else string.ascii_uppercase
        )
        for i in range(10)
    ]
    return "".join(filename)


async def decode_qr(filepath: str) -> str:
    """Декодировать изображение QR-кода."""
    decocdeQR = decode(Image.open(filepath))
    return decocdeQR[0].data.decode("ascii")


async def delete_file(path: str, file_name: str):
    """Удалить файл в заданной директории"""
    try:
        os.remove(path / (file_name + FMT_JPG))
    except:
        logger("Ошибка удаления файла")


async def delete_files_in_folder(folder_path: str):
    """Удаление всех файлов в заданной директории"""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            logger(f"Ошибка при удалении файла {file_path}. {e}")


async def download_file(file, destination) -> str:
    """
    Скачать файл.
    Генерируется имя, скачивается файл из бота и
    сохраняется в назначенной директории.
    """
    logger()
    file_name = await generate_filename()
    filename_with_format = file_name + FMT_JPG
    path = destination / (file_name + FMT_JPG)
    file_from_bot = await bot.get_file(file.file_id)
    destination_file = await bot.download_file(
        file_from_bot.file_path, os.path.join(os.getcwd(), path)
    )
    return file_name


async def get_code_image(filename: str):
    """Получить необходимый файл по имени."""
    pass


async def validate_photo(message: Message) -> bool:
    """
    Валидцация полученного изображения.
    Передается объект сообщения,
    далее вызов функции загрузки файла, он возращает имя файла
    в случае успешной загрузки.
    Загруженный файл(qr-код) декодируется и проверяется регуляркой
    на соответствие - если True -в значение value записываются
    последние три цифры кода.
    Функция возвращает словарь со значениями client_id и encode_value.
    """

    result_data: dict[str] = {"client_id": None, "encode_value": None}
    buffer = await download_file_from_bot(message)
    decoded_qr = await decode_qr(buffer)
    logger(decoded_qr)
    if re.fullmatch(REGEX_QR_PATTERN, decoded_qr):
        client_id, value = decoded_qr.split("_")
        encode_value = await encode_data(value)
        result_data["client_id"] = client_id
        result_data["encode_value"] = encode_value
    logger(result_data)
    return result_data


async def get_user_data(user_id: int) -> str:
    """Получить данные пользователя."""
    try:
        user = await UsersDAO.get_user_full_data(user_id)
        logger(user)
        result = (
            f"Ваши данные 📂: \n\n"
            f"Юзернэйм 📱:    {user.username}\n"
            f"Рабочий ID 🔮:    {user.manager_id}\n"
            f"Адрес пункта 🏚:    {user.addres}\n"
        )
        n_type = f"Уведомления:  {user.notice_type}\n"
        return (
            result + f"ID пункта: {user.point_id}\n" + n_type
            if user.point_id != 1
            else result + n_type
        )
    except Exception as error:
        logger(error)
        return "Ошибка получения данных"


async def get_point_list_caption(point_list: dict[int, Points]) -> str:
    """Получить описание к списку пунктов.
    Передается список объектов модели Point,
    на основе этих данных создается строка-описание к фото."""
    logger()
    point_list.pop(1, None)
    if not point_list:
        caption = "Вы не выбрали пункт"
    else:
        caption = "Выбранные пункты: \n\n"
        for point in point_list.values():
            caption += f"ID {point.point_id} {point.addres} \n"
    return caption


async def get_notice_type(user_id: int) -> str:
    """Получить описание к меню с режимом уведомлений.
    По id пользователя находит объект его уведомлений,
    если его нет - то создает объект модели в бд."""
    caption = "Режим уведомлений: {}"
    notice = await SchedulesDAO.get_by_attribute("user_id", user_id)
    logger(notice, NOTIFICATION_TYPE)
    if notice:
        for n_type in NOTIFICATION_TYPE:
            logger(n_type, notice.notice_type.code)
            if notice.notice_type in n_type:
                return caption.format(n_type[1])
    return caption.format("ВЫКЛ")


async def delete_file(path: str):
    """Удалить файл в заданной директории"""
    try:
        os.remove(path)
    except:
        logger("Ошибка удаления файла")


async def read_excel_file(message: Message):
    """Обработка данных эксель файла."""

    xlsx_file_in_buffer = await download_file_from_bot(message)
    workbook = openpyxl.load_workbook(xlsx_file_in_buffer)
    sheet = workbook.active
    return [
        {"point_id": row[0], "addres": row[1]}
        for row in sheet.iter_rows(values_only=True)
    ]


async def download_file_from_bot(message: Message) -> BytesIO:
    """Загрузка файла из бота в буфер."""

    buffer = BytesIO()
    if message.content_type == ContentType.PHOTO:
        file_from_bot = await bot.get_file(message.photo[-1].file_id)
    elif message.content_type == ContentType.DOCUMENT:
        file_from_bot = await bot.get_file(message.document.file_id)
    return await bot.download_file(file_from_bot.file_path, buffer)
