from datetime import datetime
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship


from app.users.constants import MOSCOW_TZ
from app.core.database import Base


class Acces_Codes(Base):

    value = Column(String, nullable=False)
    limit = Column(Integer, nullable=True)
