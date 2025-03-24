from datetime import datetime
from sqlalchemy import and_, insert, select
from sqlalchemy.exc import SQLAlchemyError

from app.core.constants import EXPIRED
from app.dao.base import BaseDAO, ModelType
from app.core.database import async_session_maker
from app.core.logging import logger
from app.sale_codes.models import SaleCodes
from app.trades.models import Trades
from app.users.models import Users


class TradesDAO(BaseDAO):
    """Класс CRUD-операций с моделью обменов кодами."""

    model = Trades

    @classmethod
    async def get_trade_by_point(cls, point_id: int) -> ModelType:
        """
        Получить актуальные объекты моделей БД.
        Возвращает список объектом переданой модели,
        созданные в день запроса.
        """
        today = datetime.now().date()
        async with async_session_maker() as session:
            get_objs = await session.execute(
                select(Trades.__table__.columns, SaleCodes.__table__.columns)
                .join(
                    SaleCodes,
                    Trades.sale_code_id == SaleCodes.id,
                    isouter=True,
                )
                .where(
                    and_(
                        Trades.point_id == point_id,
                        Trades.created_at == today,
                        SaleCodes.created_at == today,
                    )
                )
            )
            return get_objs.mappings().first()

    @classmethod
    async def create_or_update_trade(cls, data: dict):
        """Обновить или создать трейд.
        Запрос в бд на существование трейда с переданным sale_code_id,
        если такой есть - обновляет у него дату создания,
        если нет - создает объект модели с переданными данными.
        """
        async with async_session_maker() as session:
            try:
                trade = await session.execute(
                    select(Trades.__table__.columns).filter_by(**data)
                )
                logger(trade)
                trade = trade.mappings().all()
                if not trade:
                    await session.execute(insert(cls.model).values(**data))
                    await session.commit()
                    return True
                await TradesDAO.update(trade, data)
                return True
            except (SQLAlchemyError, Exception) as error:
                await session.rollback()
                if isinstance(error, SQLAlchemyError):
                    message = "Database Exception"
                elif isinstance(error, Exception):
                    message = "Unknown Exception"
                message += ": Не удается добавить данные."
                logger(error, message)
