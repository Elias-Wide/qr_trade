"""Модуль содержит заглушку на выполнение неподдерживаемых команд."""

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from app.bot.filters import BanFilter, UserExistFilter
from app.core.config import settings

echo_router = Router()
ban_router = Router()
ban_router.message.filter(~BanFilter())


@echo_router.message()
async def send_echo(message: Message) -> None:
    """Возвращает текст при получении неподдерживаемой команды."""
    await message.reply(
        f"На данный момент я не поддерживаю команду {message.text} 🤷\n\n"
        f"Могу предложить вам обратиться к @{settings.telegram.admin_username} "
        "с предложением по улучшению бота или багрепортом."
    )


@ban_router.message()
async def send_banned_message(message: Message) -> None:
    """Возвращает текст для забаненного пользователя."""
    await message.reply("Вам заблокирован доступ к боту.")
