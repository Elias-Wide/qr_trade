from pathlib import Path
from typing import Optional

from cryptography.fernet import Fernet
from pydantic import Field, SecretStr, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
QR_DIR = STATIC_DIR / "qr"


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class AuthConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="app_")
    logging_mode: str = "on"
    admin_email: str
    admin_password: SecretStr
    admin_sc: SecretStr
    secret_key: Optional[SecretStr] = Field(default=None)

    @field_validator("secret_key", mode="before")
    @classmethod
    def assemble_secret_key(
        cls, v: Optional[str], values: ValidationInfo
    ) -> str:
        if v is None:
            return Fernet.generate_key()
        return v.encode()

    def refresh_secret_key(self):
        self.secret_key = Fernet.generate_key()


class TelegramConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="tg_")

    bot_token: SecretStr
    admin_username: str
    admin_id: int
    webhook_host: str


class DatabaseConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="db_")

    host: str
    name: str
    password: SecretStr
    port: int
    user: str
    url: Optional[str] = Field(default=None)

    @field_validator("url", mode="before")
    @classmethod
    def assemble_url(cls, v: Optional[str], values: ValidationInfo) -> str:
        if v is None:
            return (
                f"postgresql+asyncpg://{values.data['user']}:"
                f"{values.data['password'].get_secret_value()}@{values.data['host']}:"
                f"{values.data['port']}/{values.data['name']}"
            )
        return v


class Settings(BaseSettings):
    telegram: TelegramConfig = Field(default_factory=TelegramConfig)
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    auth: AuthConfig = Field(default_factory=AuthConfig)

    @classmethod
    def load(cls) -> "Config":
        return cls()


settings = Settings.load()
