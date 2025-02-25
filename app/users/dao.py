from sqlalchemy import insert, select
from sqlalchemy.orm import aliased

from app.core.logging import logger
from app.dao.base import BaseDAO
from app.core.database import async_session_maker
from app.points.models import Points
from app.sale_codes.models import Sale_Codes
from app.schedules.models import Schedules
from app.users.models import Users


class UsersDAO(BaseDAO):
    """Класс CRUD-операций с пользователями."""

    model = Users

    @classmethod
    async def get_user_full_data(cls, user_id: int):
        """
        Запрос в базу данных для получения полной информации.
        Возвращает данные о пользователе по телеграм id,
        включаюя данные рабочего офиса пользователя.
        """
        async with async_session_maker() as session:
            logger()
            get_user = await session.execute(
                select(
                    Users.__table__.columns,
                    Points.__table__.columns,
                    Schedules.notice_type,
                )
                .join(Users.schedule)
                .join(Users.points)
                .where(Users.id == user_id)
            )

        return get_user.mappings().all()[0]

    @classmethod
    async def change_point(telegram_id: int, point_id: int):
        async with async_session_maker() as session:
            get_user = await session.execute(
                select(Users.__table__.columns).where(
                    Users.telegram_id == telegram_id
                )
            )
