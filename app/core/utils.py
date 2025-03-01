import base64
import os

from cryptography.fernet import Fernet
from passlib.context import CryptContext
import segno
from pyzbar.pyzbar import decode
from PIL import Image

from app.core.config import STATIC_DIR, settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# key = settings.auth.secret_key


async def encode_data(data: str) -> str:
    bytes_data = str(data).encode()
    """Кодирование."""
    return str(
        (
            Fernet(settings.auth.secret_key.get_secret_value()).encrypt(
                bytes_data
            )
        ).decode()
    )


async def decode_data(value: bytes) -> int:
    """Декодирование"""
    return (
        Fernet(settings.auth.secret_key.get_secret_value())
        .decrypt(value.encode())
        .decode("utf-8")
    )


async def is_file_in_dir(name, path):
    """Проверить, если ли необходимое изображение в директории."""
    for root, dirs, files in os.walk(path):
        if name in files:
            return True
        return False
