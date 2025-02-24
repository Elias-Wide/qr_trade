from sqlalchemy import and_, func, insert, select
from app.dao.base import BaseDAO
from app.core.database import async_session_maker
from app.notifications.models import Notifications
from app.points.models import Points
from app.core.logging import logger

class NotificationsDAO(BaseDAO):
    model = Notifications

    @classmethod
    async def set_nonification_type(cls, user_id: int, notice_type: str):
        """Установить тип уведомлений пользователя."""
        async with async_session_maker() as session:
            logger()
            obj = await session.execute(
                select(cls.model.__table__.columns).where(Notifications.user_id == user_id))
            if not obj:
                obj = await cls.create(
                    {
                        "user_id": user_id,
                        "notice_type": notice_type
                    }
                )
            obj.notice_type = notice_type
            await session.commit()
            await session.refresh(obj)