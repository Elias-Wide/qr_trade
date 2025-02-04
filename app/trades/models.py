from datetime import datetime
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


from app.core.database import Base
from app.users.constants import MOSCOW_TZ


class Trades(Base):
    """Модель Trades.
    Обеспечивает связь записей между пользователями и пунктами,
    на которые сделаны заказы.
    """

    user_id = Column(ForeignKey("users.id"))
    point_id = Column(ForeignKey("points.id"))
    users = relationship("Users", back_populates="trades")
    point = relationship("Points", back_populates="trades")
    created_at = Column(Date, default=datetime.now)


# ^\d{6,}_\d{5}