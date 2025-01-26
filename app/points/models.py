from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


from app.database import Base


class Points(Base):

    point_id = Column(Integer, nullable=False, unique=True)
    addres = Column(String, nullable=False)
    managers = relationship("Users", back_populates="managers")
    codes = relationship("Codes", back_populates="")
