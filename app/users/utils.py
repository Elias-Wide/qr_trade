import base64

from cryptography.fernet import Fernet
from passlib.context import CryptContext

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
key = Fernet.generate_key() 
id = 567890

def encode_id(id: bytes, key: bytes) -> str:
    """Кодирование id"""
    return str((Fernet(key).encrypt(id)).decode())

def decode_id(value: bytes, key: bytes) -> int:
    """Декодирование id"""
    return int(Fernet(key).decrypt(value))


x = encode_id(str(id).encode(), key)
print(type(x))
x = decode_id(x, key)
print(type(x))
# print(Fernet.generate_key())

print(key) 
# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)