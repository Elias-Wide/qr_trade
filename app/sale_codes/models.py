from datetime import datetime
from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship


from app.core.database import Base


class Sale_Codes(Base):
    """
    Модель Sale_Codes.
    Коды подтверждения продаж.
    """

    user_id = Column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(Date, default=datetime.now)
    client_id = Column(String, nullable=False, unique=True)
    encoded_value = Column(String, nullable=False)
    user = relationship("Users", back_populates="codes")
    trades = relationship(
        "Trades",
        cascade="all, delete-orphan",
        backref="sale_code",
    )
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "client_id",
            name="unique_user_and_client_id",
        ),
    )

    def __str__(self):
        return f"Код #{self.client_id}"
