from datetime import datetime
from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship


from app.core.database import Base
from app.users.constants import MOSCOW_TZ


class Sale_Codes(Base):
    """
    Модель Sale_Codes.
    Коды подтверждения продаж.
    """

    user_id = Column(ForeignKey("users.id"), nullable=False)
    created_at = Column(Date, default=datetime.now)
    file_name = Column(String, nullable=False)
    value = Column(String, nullable=False, unique=True)
    trades = relationship(
        "Trades", cascade="all,delete", back_populates="sale_codes"
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "value",
            name="unique_user_id_and_value",
        ),
    )
