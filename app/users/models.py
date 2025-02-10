from sqlalchemy import BOOLEAN, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


from app.users.constants import MOSCOW_TZ
from app.core.database import Base
from app.points.models import Points
from app.sale_codes.models import Sale_Codes
from app.trades.models import Trades


class Users(Base):
    """Модель пользователя.

    Args:
        telegram_id: user_id в телеграмме
        username: имя пользователя в телеграмме
        employee_id: рабочий id
        point: id пункта менеджера
        timezone: временной пояс
        point: пункт менеджера
        hashed_code: хэшированный код подтверждения
    """

    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=False)
    point_id = Column(ForeignKey("points.id"), nullable=True)
    manager_id = Column(Integer, unique=True, nullable=False)
    timezone = Column(Integer, default=MOSCOW_TZ)
    ban = Column(BOOLEAN, default=False)
    # sale_codes = relationship("Sale_codes", back_populates="managers")
    points = relationship("Points", back_populates="managers")
    trades = relationship("Trades", back_populates="users")
