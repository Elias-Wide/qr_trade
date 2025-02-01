from sqlalchemy import BOOLEAN, Column, Integer, String
from sqlalchemy.orm import relationship


from app.users.constants import MOSCOW_TZ
from app.core.database import Base


class Users(Base):
    """Модель пользователя.

    Args:
        tg_user_id: user_id в телеграмме
        username: имя пользователя в телеграмме
        hashed_wb_id: кодированный клиентский wb_id
        employee_id: рабочий id
        point: id пункта менеджера
        timezone: временной пояс
        point: пункт менеджера
        hashed_code: хэшированный код подтверждения
    """

    tg_user_id = Column(Integer, nullable=False)
    username = Column(String, nullable=False)
    wb_id = Column(Integer, nullable=False)
    point_id = Column(Integer, nullable=True)
    manager_id = Column(Integer, nullable=False)
    timezone = Column(Integer, default=MOSCOW_TZ)
    ban = Column(BOOLEAN , default=False)
    code = relationship("Sale_Codes", back_populates="user")
    point = relationship("Points", back_populates="user")
    trades = relationship("Trades", back_populates="user")
