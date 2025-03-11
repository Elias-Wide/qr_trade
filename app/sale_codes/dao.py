from datetime import datetime, timedelta
from sqlalchemy import and_, func, insert, select
from app.core.constants import TIMEZONE_RU
from app.dao.base import BaseDAO, ModelType
from app.core.database import async_session_maker
from app.sale_codes.models import Sale_Codes
from app.users.constants import MOSCOW_TZ
from pytz import timezone


class Sale_CodesDAO(BaseDAO):
    """Класс CRUD-операций с моделью обменов кодами."""

    model = Sale_Codes

    @classmethod
    async def create_code_or_update(
        cls,
        user_id: int,
        client_id: str,
        encoded_value: str,
        user_tz: int = MOSCOW_TZ,
    ) -> str:
        """
        Создать или обновить объект кода.
        Передаются данные для создания объекта,
        если объект с заданным user_id и value уже существует,
        то обновляются его значения и удаляется соответствующее
        фото из хранилища.
        В противном случае создается новый объект модели."""
        async with async_session_maker() as session:
            today = datetime.now(timezone(TIMEZONE_RU[user_tz]))
            today = today.replace(tzinfo=None)
            user_code = await session.scalars(
                select(cls.model).where(
                    and_(
                        cls.model.user_id == user_id,
                        cls.model.client_id == client_id,
                    )
                )
            )
            user_code = user_code.first()
            if not user_code:
                query = insert(cls.model).values(
                    user_id=user_id,
                    client_id=client_id,
                    created_at=today,
                    encoded_value=encoded_value,
                )
                await session.execute(query)
                await session.commit()
                answer = "create"
            else:
                user_code.client_id = client_id
                user_code.encoded_value = encoded_value
                user_code.created_at = today
                await session.commit()
                await session.refresh(user_code)
                answer = "update"
            return answer

    @classmethod
    async def get_user_qr(cls, user_id: int, user_tz=MOSCOW_TZ):
        async with async_session_maker() as session:
            today = datetime.now(timezone(TIMEZONE_RU[user_tz]))
            today = today.replace(tzinfo=None)
            get_user = await session.execute(
                select(cls.model.__table__.columns).where(
                    and_(
                        cls.model.user_id == user_id,
                        cls.model.created_at == today.date(),
                    )
                )
            )
            return get_user.mappings().all()

    # @classmethod
    # async def get_codes_by_attribute(
    #     cls,
    #     attr_name: str,
    #     attr_value: str,
    # ) -> list[ModelType | None]:
    #     """Возвращает объект по заданому атрибуту."""
    #     async with async_session_maker() as session:
    #         db_objs = await session.execute(
    #             select(cls.model.__table__.columns).where(
    #                 getattr(cls.model, attr_name) == attr_value,
    #             ),
    #         )
    #         return db_objs.mappings().all()
