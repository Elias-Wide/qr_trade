from typing import List
from sqlalchemy import JSON, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType
from app.bot.constants import NOTIFICATION_TYPE
from app.core.database import Base


class Schedules(Base):
    """Модель уведомлений."""

    notice_type = Column(
        ChoiceType(NOTIFICATION_TYPE), default=NOTIFICATION_TYPE[0][0]
    )
    user_id = Column(ForeignKey("users.id"), nullable=False)
    schedule = Column(JSON, nullable=True)
    user = relationship("Users", back_populates="schedule")
