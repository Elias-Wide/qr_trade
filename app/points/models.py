from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


from app.core.database import Base
from app.core.config import settings

class Points(Base):
    """Модель wb офиса."""

    point_id = Column(Integer, nullable=False, unique=True)
    addres = Column(String, nullable=False)

settt = settings