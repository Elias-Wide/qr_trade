"""Фильтры участка анкеты."""

from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import QR_DIR
from app.points.dao import PointsDAO
from app.bot.utils import download_file, validate_photo
from app.points.models import Points
from app.sale_codes.dao import Sale_CodesDAO
from app.users.dao import UsersDAO
from app.core.logging import logger


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
        logger()
        if self.attr_name == "telegram_id":
            attr_value = message.from_user.id
        else:
            attr_value = int(message.text)
        obj = await self.modelDAO.get_by_attribute(
            attr_name=self.attr_name, attr_value=attr_value
        )
        if obj:
            return {self.attr_name: attr_value, "model_obj": obj}
        logger(False)
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
        self.attr_name = "point_id"


class AccesCodeFilter(BaseFilter):
    """Класс валидации кода доступа к боту."""

    async def __call__(self, message: Message) -> bool:
        if message.text.strip() == "wb123":
            return True
        return False


class ImgValidationFilter(BaseFilter):
    """
    Класс фильтрации загруженного пользователем изображения.
    Вызов функции валидации.
    Возвращает словарь с данными file_name и value.
    """

    async def __call__(self, message: Message) -> dict[str] | bool:
        validated_data: dict[str] = await validate_photo(message)
        logger(validated_data)
        if all(validated_data.values()):
            return validated_data
        return False


class BanFilter(UserExistFilter):
    """Класс фильтрации по наличию бана у пользователя."""

    async def __call__(self, message):
        """
        Проверить пользователя на наличие бана.
        Делает базовую проверку на регистрацию из родительского класса
        и проверяет на наличие бана.
        """
        user = await super().__call__(message)
        if user and user["model_obj"].ban == True:
            return False
        return user
