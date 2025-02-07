from typing import List
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


from app.core.database import Base
from app.core.config import settings


class Points(Base):
    """Модель офиса.

    Args:
        name: короткое имя
        point_id: id фоиса
        addres: полный адрес
        trades: созданные модели обмена кодами
        managers: менеджеры офиса
    """

    name = Column(String, nullable=False, unique=True)
    point_id = Column(Integer, nullable=False, unique=True)
    addres = Column(String, nullable=False)
    trades = relationship("Trades", back_populates="point")
    managers = relationship("Users", back_populates="points")
