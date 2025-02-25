from datetime import date
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
        """
        Установить тип уведомлений пользователя.
        Находить модель Schedules по юзер id,
        если таког объекта нет - создает.
        """
        async with async_session_maker() as session:
            logger()
            obj = await session.scalars(
                select(cls.model).where(Schedules.user_id == user_id)
            )
            obj = obj.first()
            if not obj:
                obj = await cls.create(
                    {"user_id": user_id, "notice_type": notice_type}
                )
            else:
                logger(obj)
                obj.notice_type = notice_type
            await session.commit()
            await session.refresh(obj)
    
    @classmethod
    async def get_user_schedule(cls, user_id: int) -> list[str]:
        async with async_session_maker() as session:
            list_date = await session.scalars(
                select(cls.model.schedule).where(
                    cls.model.user_id == user_id
                )
            )
            logger(list_date)
            return list_date.all()
    
    @classmethod
    async def set_schedule(cls, user_id: int, date_list: list[str]) -> bool:
        async with async_session_maker() as session:
            try:
                user_schedule = await session.scalars(
                    select(cls.model).where(
                        cls.model.user_id == user_id
                    )
                )
                user_schedule = user_schedule.first()
                logger(user_schedule, date_list)
                if not user_schedule:
                    SchedulesDAO.create({
                        "user_id": user_id,
                        "schedule": date_list
                    })
                else:
                    user_schedule.schedule = date_list
                await session.commit()
                await session.refresh(user_schedule)
                return True
            except:
                logger("SET SCHEDULE ERROR")
                return False