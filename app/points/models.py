from typing import List
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


from app.core.database import Base
from app.core.config import settings


def same_as(column_name):
    def default_function(context):
        return context.current_parameters.get(column_name)

    return default_function


class Points(Base):
    """Модель офиса.

    Args:
        point_id: id офиса
        addres: полный адрес
        trades: созданные модели обмена кодами
        managers: менеджеры офиса
    """

    addres = Column(String, nullable=False)
    point_id = Column(Integer, nullable=False, unique=True)
    region_id = Column(
        ForeignKey("regions.id", ondelete="SET NULL"), nullable=True
    )
    name = Column(String, nullable=True, default=same_as("addres"))
    region = relationship("Regions", back_populates="points")
    trades = relationship("Trades", back_populates="point")
    managers = relationship("Users", back_populates="points")

    def __str__(self):
        return f"{self.addres}"
