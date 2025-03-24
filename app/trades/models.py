from datetime import datetime
from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref

from app.core.database import Base
from app.users.constants import MOSCOW_TZ
from app.sale_codes.models import SaleCodes


class Trades(Base):
    """Модель Trades.
    Обеспечивает связь записей между пользователями и пунктами,
    на которые сделаны заказы.
    """

    sale_code_id = Column(
        ForeignKey("sale_codes.id"),
        nullable=False,
    )
    user_id = Column(ForeignKey("users.id"))
    point_id = Column(ForeignKey("points.point_id"), nullable=False)
    users = relationship("Users", back_populates="trades")
    point = relationship("Points", back_populates="trades")
    created_at = Column(Date, default=datetime.now)

    __table_args__ = (
        UniqueConstraint(
            "sale_code_id",
            "user_id",
            "point_id",
            name="unique_user_point_sale_code_id",
        ),
        UniqueConstraint(
            "sale_code_id",
            "id",
            name="unique_sale_code_id",
        ),
    )

    def __str__(self):
        return f"код для офиса {self.point_id}"
