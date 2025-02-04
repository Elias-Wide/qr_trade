from datetime import datetime
from sqlalchemy import insert, select
from app.dao.base import BaseDAO
from app.core.database import async_session_maker
from app.sale_codes.models import Sale_Codes
from app.sale_codes.utils import generate_filename
from app.trades.models import Trades
from app.users.constants import MOSCOW_TZ
from app.users.models import Users


class Sale_CodesDAO(BaseDAO):
    """Класс CRUD-операций с моделью обменов кодами."""

    model = Sale_Codes
    
    @classmethod
    async def create_code(cls, user_id: int, file_name: str):
        async with async_session_maker() as session:
            query = insert(cls.model).values(
                user_id=user_id,
                file_name=file_name,
                created_at=datetime.now(tz=MOSCOW_TZ)
            )
            await session.execute(query)
            await session.commit()
