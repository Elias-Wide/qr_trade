from sqlalchemy import select

from app.dao.base import BaseDAO
from app.core.database import async_session_maker
from app.sale_codes.models import Sale_Codes


class Sale_CodesDAO(BaseDAO):
    """Crud-операции класса кода подтверждения продажи."""
    model = Sale_Codes
