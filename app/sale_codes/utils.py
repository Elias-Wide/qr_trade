import os
import random
import string

import segno

from app.core.config import STATIC_DIR
from app.core.logging import get_logger

logger = get_logger(__name__)


async def generate_filename() -> str:
    """Генерирует рандомное имя для файла."""
    filename = [
        random.choice(
            string.ascii_lowercase + string.digits if i != 5 else string.ascii_uppercase
        )
        for i in range(10)
    ]
    return "".join(filename)


def create_qr(data: str, file_name: str):
    """Создать QR-код из строки и сохранить в папку статики."""
    qrcode = segno.make_qr(data)
    qrcode.save(
        STATIC_DIR / "trades" / file_name,
        scale=10,
    )


def delete_files_in_folder(folder_path: str):
    """Удаление файлов в заданной директории"""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            logger.error(f"Ошибка при удалении файла {file_path}. {e}")
