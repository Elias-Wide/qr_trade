from typing import List
from sqlalchemy import ARRAY, JSON, Column, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType
from app.core.constants import NOTIFICATION_TYPE
from app.core.database import Base


class Schedules(Base):
    """Модель уведомлений."""

    notice_type = Column(
        ChoiceType(NOTIFICATION_TYPE), default=NOTIFICATION_TYPE[0][0]
    )
    user_id = Column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    schedule = Column(ARRAY(Date), default=[])
    user = relationship("Users", back_populates="schedule")

    def __str__(self):
        return f"График пользователя {self.user_id}"
