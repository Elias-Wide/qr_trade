"""Фильтры участка анкеты."""

from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.points.dao import PointsDAO
from app.users.dao import UsersDAO


class BaseUserFilter(BaseFilter):
    """Базовый класс фильтрации пользователя по параметрам."""

    model_attr = None

    def __init__(self) -> None:
        pass

    async def __call__(
        self,
        message: Message,
        session: AsyncSession,
    ) -> bool | dict[str, int]:
        value = int(message.text.strip())
        if not await UsersDAO.get_by_attribute(
            attr_name=self.model_attr,
            attr_value=value,
            session=session,
        ):
            return {self.model_attr: value}
        return False


class UserTgIdFilter(BaseUserFilter):
    """Фильтрация по телеграмм id."""

    def __init__(self) -> None:
        self.model_attr = "tg_user_id"


class ManagerIdFilter(BaseUserFilter):
    """Фильтрация по manager id."""

    def __init__(self) -> None:
        self.model_attr = "manager_id"


class ClientIdFilter(BaseUserFilter):
    """Фильтрация по client id."""

    def __init__(self) -> None:
        self.model_attr = "client_id"


class PointIdFilter(BaseFilter):
    """Фильтрация по point id."""

    def __init__(self) -> None:
        self.model_attr = "point_id"

    def __call__(
        self,
        message: Message,
        session: AsyncSession,
    ) -> bool:
        value = int(message.text.strip())
        if not value:
            value = None
        is_point_exist = await PointsDAO.get_by_attribute(
            attr_name="id", attr_value=value, session=session
        )
        if not is_point_exist:
            return False
        return {self.model_attr: value}
