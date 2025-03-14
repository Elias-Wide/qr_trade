from typing import List
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


from app.core.database import Base
from app.core.config import settings


class Regions(Base):
    """Модель региона.

    Args:
    ceo_id: id пользователя руководителя региона, если он есть в бд.
    name: название региона
    points: связь с моделью points
    """

    ceo_id = Column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    name = Column(String, nullable=False, unique=True)
    points = relationship("Points", back_populates="region")
    ceo = relationship("Users", backref="region")

    def __str__(self):
        return f"Регион {self.name}"
