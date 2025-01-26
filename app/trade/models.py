from datetime import datetime
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship


from app.core.database import Base
from app.users.constants import MOSCOW_TZ


class Trades(Base):
    """Модель Trades.
    Обеспечивает связь записей между пользователями и пунктами,
    на которые сделаны заказы.
    """
    user = relationship("users", back_populates="trade")
    point = relationship("Points", back_populates='trade')
    created_at = Column(Date, default=datetime.now)
