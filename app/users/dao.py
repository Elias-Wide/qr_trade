from datetime import datetime
from sqlalchemy import and_, any_, insert, or_, select
from sqlalchemy.orm import aliased

from app.core.logging import logger
from app.dao.base import BaseDAO
from app.core.database import async_session_maker
from app.points.models import Points
from app.sale_codes.models import Sale_Codes
from app.schedules.models import Schedules
from app.trades.models import Trades
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
                    Points.point_id,
                    Points.addres,
                    Schedules.schedule,
                    Schedules.notice_type,
                )
                .join(Schedules, Schedules.user_id == Users.id, isouter=True)
                .join(Points, Points.point_id == Users.point_id, isouter=True)
                .where(Users.id == user_id)
            )
        data = get_user.mappings().all()[0]
        logger(data)
        return data

    @classmethod
    async def change_point(telegram_id: int, point_id: int):
        async with async_session_maker() as session:
            get_user = await session.execute(
                select(Users.__table__.columns).where(
                    Users.telegram_id == telegram_id
                )
            )

    @classmethod
    async def get_telegram_id(cls) -> list[int]:
        """
        Получить список id пользователей.
        Возвращает список telegram id пользователей,
        которые должны получить уведомление о наличие заказов.
        У пользователя должны быть включены уведомления, либо уведомления
        по графику(и установлен рабочий график) и текущая дата есть в графике.
        """

        # SELECT * FROM public.users
        # LEFT JOIN schedules ON users.id = schedules.user_id
        # LEFT JOIN trades ON trades.point_id = users.point_id
        # WHERE trades.id IS NOT NULL
        # AND (
        #         (
        #             notice_type = 'by_schedule'
        #             today = ANY(schedule)
        #         )
        #         OR notice_type = 'always'
        # )
        async with async_session_maker() as session:
            today = datetime.now().date()
            get_users_id = await session.scalars(
                select(Users.telegram_id)
                .join(Schedules, Schedules.user_id == Users.id, isouter=True)
                .join(Trades, Users.point_id == Trades.point_id, isouter=True)
                .where(
                    and_(
                        Trades.id.isnot(None),
                        or_(
                            Schedules.notice_type == "always",
                            and_(
                                Schedules.notice_type == "by_schedule",
                                any_(Schedules.schedule) == today,
                            ),
                        ),
                    )
                )
            )
            return get_users_id.all()
