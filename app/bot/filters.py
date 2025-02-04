"""Фильтры участка анкеты."""

from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.points.dao import PointsDAO
from app.users.dao import UsersDAO


class UserTgIdFilter(BaseFilter):
    """Базовый класс фильтрации пользователя по параметрам."""

    def __init__(self) -> None:
        pass

    async def __call__(
        self,
        message: Message
    ) -> bool:
        if not await UsersDAO.get_by_id(message.from_user.id):
            return True
        return False


class ManagerIdFilter(BaseFilter):
    """Фильтрация по manager id."""

    def __init__(self, *args) -> None:
        self.model_attr = "manager_id"
    
    async def __call__(self, message: Message):
        id = int(message.text.strip())
        if not await UsersDAO.get_by_attribute(
            attr_name=self.model_attr,
            attr_value=id
        ):
            return True
        return False
        


class PointIdFilter(BaseFilter):
    """Фильтрация по point id."""

    def __init__(self) -> None:
        self.model_attr = "point_id"

    async def __call__(
        self,
        message: Message,
    ) -> bool:
        value = int(message.text.strip())
        if not value:
            value = 1
        is_point_exist = await PointsDAO.get_by_attribute(
            attr_name="id", attr_value=value
        )
        if not is_point_exist:
            return False
        return True


class AccesCodeFilter(BaseFilter):
    
    async def __call__(self, message: Message) -> bool:
        print(message.text)
        if message.text.strip() == 'wb123':
            print('УСПЕШНО!Ц!')
            return True
        return False