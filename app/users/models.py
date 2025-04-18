from sqlalchemy import (
    BOOLEAN,
    BigInteger,
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship


from app.users.constants import MOSCOW_TZ
from app.core.database import Base
from app.points.models import Points
from app.sale_codes.models import SaleCodes
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

    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String, nullable=False)
    ban = Column(BOOLEAN, default=False)
    manager_id = Column(Integer, unique=True, nullable=False)
    point_id = Column(ForeignKey("points.id"), nullable=True)
    timezone = Column(Integer, default=MOSCOW_TZ)
    codes = relationship("SaleCodes", cascade="delete", back_populates="user")
    points = relationship("Points", back_populates="managers")
    trades = relationship(
        "Trades", cascade="all,delete", back_populates="users"
    )
    schedule = relationship(
        "Schedules", cascade="delete", back_populates="user"
    )

    def __str__(self):
        return f"Пользователь @{self.username}"
