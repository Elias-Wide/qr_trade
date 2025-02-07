from sqlalchemy import insert
from app.dao.base import BaseDAO
from app.core.database import async_session_maker
from app.trades.models import Trades
from app.users.models import Users


class TradesDAO(BaseDAO):
    """Класс CRUD-операций с моделью обменов кодами."""

    model = Trades
