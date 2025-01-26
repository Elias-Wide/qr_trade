from sqlalchemy import insert
from app.dao.base import BaseDAO
from app.core.database import async_session_maker
from app.users.models import Users


class UsersDAO(BaseDAO):
    """Класс CRUD-операций с пользователями."""
    model = Users