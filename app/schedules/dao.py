from sqlalchemy import and_, func, insert, select
from app.bot.constants import N_TYPE_DICT
from app.dao.base import BaseDAO
from app.core.database import async_session_maker
from app.schedules.models import Schedules
from app.points.models import Points
from app.core.logging import logger


class SchedulesDAO(BaseDAO):
    model = Schedules

    @classmethod
    async def set_nonification_type(cls, user_id: int, notice_type: str):
        """Установить тип уведомлений пользователя."""
        async with async_session_maker() as session:
            logger()
            obj = await session.scalars(
                select(cls.model).where(
                    Schedules.user_id == user_id
                )
            )
            logger(obj)
            obj = obj.first()
            logger(obj, notice_type)
            if not obj:
                obj = await cls.create(
                    {"user_id": user_id, "notice_type": notice_type}
                )
            else:
                logger(obj)
                obj.notice_type = notice_type
            await session.commit()
            await session.refresh(obj)
