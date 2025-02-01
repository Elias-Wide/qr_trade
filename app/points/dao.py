from sqlalchemy import insert
from app.dao.base import BaseDAO
from app.core.database import async_session_maker
from app.points.models import Points


class PointsDAO(BaseDAO):
    model = Points
