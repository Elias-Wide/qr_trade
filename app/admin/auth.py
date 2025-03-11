"""Модуль аутенфиукации adminpage."""

import secrets
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.core.config import settings


class AdminAuth(AuthenticationBackend):
    """Настройка бэкенда аутенфикации."""

    async def login(self, request: Request) -> bool:
        """Метод содержит логику при входе в систему."""
        form = await request.form()
        username, password = form["username"], form["password"]
        print(username, password)
        if (
            username == settings.auth.admin_email
            and password == settings.auth.admin_password.get_secret_value()
        ):
            request.session.update({"token": secrets.token_hex(16)})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        """Метод содержит логику выхода из системы."""
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        """Метод содержит логику аутенфикации."""
        token = request.session.get("token")
        if not token:
            return False
        return True


authentication_backend = AdminAuth(
    secret_key=settings.auth.admin_sc.get_secret_value()
)
