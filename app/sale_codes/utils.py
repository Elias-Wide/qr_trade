import os
import qrtools
import re
import random
import string
from pyzbar.pyzbar import decode
from PIL import Image
from aiogram.types import Message
from app.bot.constants import FMT_JPG, REGEX_QR_PATTERN
from app.core.config import QR_DIR
from app.core.logging import get_logger
from app.bot.create_bot import bot

logger = get_logger(__name__)


async def generate_filename() -> str:
    """Генерирует рандомное имя для файла."""
    filename = [
        random.choice(
            string.ascii_lowercase + string.digits if i != 5 else string.ascii_uppercase
        )
        for i in range(10)
    ]
    return "".join(filename) + FMT_JPG


# async def create_qr(data: str, file_name: str):
#     """Создать QR-код из строки и сохранить в папку статики."""
#     qrcode = segno.make_qr(data)
#     qrcode.save(
#         STATIC_DIR / "trades" / file_name,
#         scale=10,
#     )


async def decode_qr(filepath: str) -> str:
    """Декодировать изображение QR-кода."""
    decocdeQR = decode(Image.open(filepath))
    return decocdeQR[0].data.decode("ascii")


async def delete_files_in_folder(folder_path: str):
    """Удаление файлов в заданной директории"""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            logger.error(f"Ошибка при удалении файла {file_path}. {e}")


async def download_file(file, destination) -> str:
    try:
        file_name = await generate_filename()
        path = destination / file_name
        file_from_bot = await bot.get_file(file.file_id)
        destination_file = await bot.download_file(
            file_from_bot.file_path, os.path.join(os.getcwd(), path)
        )
        return file_name
    except:
        return


async def validate_photo(message: Message) -> bool:
    """
    Валидцация полученного изображения.
    Передается объект сообщения,
    далее вызов функции загрузки файла, он возращает имя файла
    в случае успешной загрузки.
    Загруженный файл(qr-код) декодируется и проверяется регуляркой
    на соответствие - если True -в значение value записываются
    последние три цифры кода.
    Если данные не проходят проверку - файл удаляется.
    Функция возвращает словарь со значениями file_name и value.
    """
    result_data: dict[str] = {
        "file_name": None,
        "value": None,
    }
    file_name = await download_file(message.photo[-1], QR_DIR)
    if file_name:
        result_data["file_name"] = file_name
        value = await decode_qr(QR_DIR / file_name)
        if re.fullmatch(REGEX_QR_PATTERN, value):
            result_data["value"] = "**" + value.split("_")[0][3:]
        else:
            os.remove(QR_DIR / file_name)
    print(result_data)
    return result_data
