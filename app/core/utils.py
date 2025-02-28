import base64

from cryptography.fernet import Fernet
from passlib.context import CryptContext
import segno
from pyzbar.pyzbar import decode
from PIL import Image

from app.core.config import STATIC_DIR, settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
key = settings.auth.secret_key


async def encode_data(data: bytes, key: bytes) -> str:
    bytes_data = str(data).encode()
    """Кодирование id"""
    return str((Fernet(key).encrypt(bytes_data)).decode())


async def decode_data(value: bytes, key: bytes) -> int:
    """Декодирование id"""
    return str(Fernet(key).decrypt(value))


x = encode_data(id, key)
print(type(x), x)
x = decode_data(x, key)
print(type(x), x)
