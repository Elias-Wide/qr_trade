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
        tg_user_id: user_id в телеграмме
        username: имя пользователя в телеграмме
        employee_id: рабочий id
        point: id пункта менеджера
        timezone: временной пояс
        point: пункт менеджера
        hashed_code: хэшированный код подтверждения
    """

    tg_user_id = Column(Integer, nullable=False)
    username = Column(String, nullable=False)
    point_id = Column(ForeignKey("points.id"), nullable=True)
    manager_id = Column(Integer, nullable=False)
    timezone = Column(Integer, default=MOSCOW_TZ)
    sale_code_id = Column(ForeignKey("sale_codes.id"))
    ban = Column(BOOLEAN , default=False)
    code = relationship("Sale_Codes", back_populates="user")
    points = relationship("Points", back_populates="managers")
    trades = relationship("Trades", back_populates="users")
