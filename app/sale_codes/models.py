from datetime import datetime
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


from app.users.constants import MOSCOW_TZ
from app.core.database import Base


class Sale_Codes(Base):

    hashed_value = Column(String, nullable=False)
    user_id = Column(ForeignKey("users.id"))
    actual_date = Column(Date, default=datetime.now)
    user = relationship("Users", back_populates="code")
