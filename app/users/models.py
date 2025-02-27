from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


from app.users.constants import MOSCOW_TZ
from app.database import Base


class Users(Base):
    """Модель пользователя.

    Args:
        tg_user_id: user_id в телеграмме
        hashed_wb_id: кодированный клиентский wb_id
        employee_id: рабочий id
        point: id пункта менеджера
        timezone: временной пояс
        point: пункт менеджера
        hashed_code: хэшированный код подтверждения
    """
    tg_user_id = Column(Integer, nullable=False)
    hashed_wb_id = Column(String, nullable=False)
    point_id = Column(Integer, nullable=True)
    employee_id = Column(String, nullable=False)
    timezone = Column(Integer, default=MOSCOW_TZ)
    point = relationship("Points", back_populates="user")
    hashed_code = relationship("Codes", back_populates="user")
