import base64

from cryptography.fernet import Fernet
from passlib.context import CryptContext

from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
key = settings.auth.secret_key


def encode_data(data: bytes, key: bytes) -> str:
    bytes_data = str(data).encode()
    """Кодирование id"""
    return str((Fernet(key).encrypt(bytes_data)).decode())

def decode_data(value: bytes, key: bytes) -> int:
    """Декодирование id"""
    return int(Fernet(key).decrypt(value))


x = encode_data(id, key)
print(type(x), x)
x = decode_data(x, key)
print(type(x), x)
# print(Fernet.generate_key())

# print(key) 
# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)