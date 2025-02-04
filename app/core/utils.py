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



def decode_qr(path: str):
    """Декодировать изображение QR-кода. """
    decocdeQR = decode(Image.open(path))
    return (decocdeQR[0].data.decode('ascii'))

def create_qr(data: str, file_name):
    """Создать QR-код из строки и сохранить в папку статики."""
    qrcode = segno.make_qr(data)
    qrcode.save(
        STATIC_DIR / "trades" / "qr_trade.png",
        scale=10,
    )
    
# create_qr('12334_12245')
print(decode_qr(STATIC_DIR / "trades" / "basic_qrcode.png"))