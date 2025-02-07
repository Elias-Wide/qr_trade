"""Фильтры участка анкеты."""

from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.points.dao import PointsDAO
from app.users.dao import UsersDAO


# class BaseUserFilter(BaseFilter):

#     def __init__(self) -> None:
#         self.modelDAO = UsersDAO
#         self.attr_name = "telegram_id"

#     async def __call__(
#         self,
#         message: Message
#     ) -> bool:
#         if not await self.modelDAO.get_by_attribute(
#             attr_name=self.attr_name,
#             attr_value=message.from_user.id
#         ):
#             return True
#         return False


class UserExistFilter(BaseFilter):
    """
    Класс фильтрации пользователя по telegram_id.
    Возвращает True для зарегистрированного пользователя.
    """

    def __init__(self) -> None:
        self.modelDAO = UsersDAO
        self.attr_name = "telegram_id"

    async def __call__(
        self,
        message: Message,
    ) -> bool:
        if self.attr_name == "telegram_id":
            attr_value = message.from_user.id
        else:
            attr_value = int(message.text)
        if attr_value and await self.modelDAO.get_by_attribute(
            attr_name=self.attr_name, attr_value=attr_value
        ):
            return True
        return False


class ManagerExistFilter(UserExistFilter):
    """
    Фильтрация по manager id.
    Если в базе уже есть такой id - возвращает False.
    """

    def __init__(self) -> None:
        self.modelDAO = UsersDAO
        self.attr_name = "manager_id"

    async def __call__(self, message):
        return not await super().__call__(message)


class PointExistFilter(UserExistFilter):
    """
    Класс фильтрации пользователя по point_id.
    Возвращает True, если офис есть в БД.
    """

    def __init__(self) -> None:
        self.modelDAO = PointsDAO
        self.attr_name = "id"


class AccesCodeFilter(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        if message.text.strip() == "wb123":
            return True
        return False
