from sqlalchemy import insert, select
from app.dao.base import BaseDAO, ModelType
from app.core.database import async_session_maker
from app.sale_codes.models import Sale_Codes
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
        async with async_session_maker() as session:
            get_objs = await session.execute(
                select(Trades.__table__.columns, Sale_Codes.__table__.columns)
                .join(Sale_Codes, Trades.sale_code_id == Sale_Codes.id, isouter=True)
                .where(Trades.point_id == point_id)
            )
            return get_objs.mappings().first()
