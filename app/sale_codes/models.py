from datetime import datetime
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


from app.core.database import Base
from app.users.constants import MOSCOW_TZ


class Sale_Codes(Base):
    """Модель Sale_Codes.
    Коды подтверждения продаж.
    """

    user_id = Column(ForeignKey("users.id"))
    trades = relationship("Trades", back_populates="trades")
    created_at = Column(Date, default=datetime.now)
    file_name = Column(String, nullable=False)