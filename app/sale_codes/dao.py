from datetime import datetime
from sqlalchemy import and_, insert, select
from app.dao.base import BaseDAO, ModelType
from app.core.database import async_session_maker
from app.sale_codes.models import Sale_Codes
from app.sale_codes.utils import generate_filename
from app.trades.models import Trades
from app.users.constants import MOSCOW_TZ, TIMEZONE_RU
from app.users.models import Users


class Sale_CodesDAO(BaseDAO):
    """Класс CRUD-операций с моделью обменов кодами."""

    model = Sale_Codes

    @classmethod
    async def create_code(cls, user_id: int, file_name: str, value: str):
        async with async_session_maker() as session:
            query = insert(cls.model).values(
                user_id=user_id,
                file_name=file_name,
                created_at=datetime.now().date(),
                value=value,
            )
            await session.execute(query)
            await session.commit()

    @classmethod
    async def get_user_qr(cls, user_id: int):
        async with async_session_maker() as session:
            get_user = await session.execute(
                select(cls.model.__table__.columns).where(
                    and_(
                        cls.model.user_id == user_id,
                        cls.model.created_at == datetime.now().date(),
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
