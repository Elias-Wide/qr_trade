from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


from app.database import Base


class Trades(Base):
    """Модель Trades.
    Обеспечивает связь записей между пользователями и пунктами,
    на которые сделаны заказы.
    """
    user = relationship("users", back_populates="trade")
    point = relationship("Points", back_populates='trade')
